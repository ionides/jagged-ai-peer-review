# Ned-Clean Analysis — w22 Project 02

---

## Human Issues

1. The profile for Beta is flat over this interval — the confidence interval of around 3-7 has not been justified.
2. Evidence of a strong nonlinear relationship between Beta and eta.
3. The conclusion "the confidence intervals of the two transmission rates are still the same" is wrong; it would be more correct to say that in both cases beta is unidentifiable over this interval.
4. The weak identifiability might suggest exploring the possibility of fixing one or more parameters at scientifically plausible values.
5. References at the end are not all cited when relevant during the main text, making it harder to see what is attributable to each reference.
6. The connection to https://kingaa.github.io/sbied/ebola/ was not made explicit, which would have strengthened the project.
7. Figure captions, figure numbers, and section numbers would make it easier for referees.
8. A benchmark likelihood (e.g., from log ARMA) is missing; a previous project's approach could be followed.

---

## Alex

**Coverage record:**
- Human Issue #1: covered (matched by finding 11 [MODERATE]: "profile spans entire search box, non-identifiability not adequately addressed")
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding 15 [MINOR]: "conclusions attribute same CI to both countries due to same search box")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed

**Findings classification:**
- Finding 1 [MAJOR] Measurement model misspecified — H used in binomial directly: A
- Finding 2 [MAJOR] Wrong population size for Sierra Leone (N=6190280 vs 16190280): A
- Finding 3 [MAJOR] Profile likelihood not constructed correctly — Beta not fixed at grid values: A
- Finding 4 [MAJOR] Funeral compartment F modeled as flow, not stock: A
- Finding 5 [MAJOR] Death rate hardcoded at exactly 50% with deterministic rounding: A
- Finding 6 [MAJOR] R0 not computed or discussed: A
- Finding 7 [MAJOR] mu_EI parameter epidemiologically implausible (~0.067 day incubation): A
- Finding 8 [MAJOR] mu_IR similarly implausible (~1 day infectious period): A
- Finding 9 [MODERATE] Search box inconsistent with initial simulation parameters (Beta=17 >> 7): C
- Finding 10 [MODERATE] F_size fixed at 50, not estimated, without justification: C
- Finding 11 [MODERATE] Profile spans entire search box — non-identifiability not adequately addressed: D (matches Human Issue #1)
- Finding 12 [MODERATE] bake() called twice for same file with different variable names: C
- Finding 13 [MODERATE] No convergence diagnostics for global search: C
- Finding 14 [MINOR] EDA superficial, does not inform model choice: C
- Finding 15 [MINOR] Conclusions attribute same CI to both countries due to same search box: D (matches Human Issue #3)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: covered (matched by finding 2 [Major]: "profile likelihood is a likelihood slice, not a profile")
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding 11 [Major]: "conclusion that Guinea and Sierra Leone have 'same transmission rate' is unsupported; identical CI bounds are artifact of search box")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: covered (matched by finding 4 [Major]: "no non-mechanistic benchmark comparison")

**Findings classification:**
- Finding 1 [Major] Measurement model applied to accumulator H — conceptually muddled: A
- Finding 2 [Major] Profile likelihood is a likelihood slice, not a profile: B (matches Human Issue #1)
- Finding 3 [Major] F_size fixed but included in log() parameter transformation: A
- Finding 4 [Major] No non-mechanistic benchmark comparison: B (matches Human Issue #8)
- Finding 5 [Major] Biologically implausible parameter estimates not discussed: A
- Finding 6 [Major] Measurement model does not include overdispersion: A
- Finding 7 [Major] rw.sd values too small for parameters on untransformed scale: A
- Finding 8 [Major] No quantitative goodness-of-fit summary reported: A
- Finding 9 [Major] Initial conditions fixed at implausible values without justification: A
- Finding 10 [Major] Sierra Leone population misspecified in simulation vs model fitting: A
- Finding 11 [Major] Conclusion that Guinea and Sierra Leone have "same transmission rate" unsupported: B (matches Human Issue #3)
- Finding 12 [Major] Funeral compartment F assigned (not accumulated) — epidemic dynamics may be incorrect: A
- Finding 13 [Major] No model diagnostics beyond visual simulation comparison: A
- Finding 14 [Major] Global search results duplicated in Guinea_params.csv: A
- Finding 15 [Major] No discussion of R0 or epidemiologically meaningful parameter summaries: A

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 12 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 0 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: covered (matched by finding 6 [Major]: "profile likelihood flat across entire box; CI uninformative")
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding 13 [Minor]: "conclusions overstate comparison between countries")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: covered (matched by finding 4 [Major]: "no benchmark comparison against non-mechanistic model")

**Findings classification:**
- Finding 1 [Major] Global search anchored to local mif2 result object: A
- Finding 2 [Major] Measurement model binomial without overdispersion: A
- Finding 3 [Major] Accumulator variable H accumulates wrong flow (dN_IR not dN_EI): A
- Finding 4 [Major] No benchmark comparison against non-mechanistic model: B (matches Human Issue #8)
- Finding 5 [Major] Population N for Sierra Leone contains factor-of-10 error: A
- Finding 6 [Major] Profile likelihood flat across entire box; CI uninformative: B (matches Human Issue #1)
- Finding 7 [Major] F_size fixed without justification: A
- Finding 8 [Major] rw.sd values very small relative to parameter scales: A
- Finding 9 [Minor] dmeas/rmeas boundary handling inconsistency: C
- Finding 10 [Minor] rm(list=ls()) inside document: C
- Finding 11 [Minor] No quantitative goodness-of-fit values reported: C
- Finding 12 [Minor] No model diagnostics beyond simulation plots and pairs plots: C
- Finding 13 [Minor] Conclusions overstate comparison between countries: D (matches Human Issue #3)
- Finding 14 [Minor] Missing pomp and package version information: C
- Finding 15 [Minor] Initial conditions fixed without sensitivity analysis: C

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: covered (matched by finding 22.02.1 [Major]: "profile likelihood for beta is flat; reported CI is not a valid confidence interval")
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding M4 [Minor]: "conclusion about equal CIs is circular")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding M6 [Minor]: "all figures lack captions")
- Human Issue #8: covered (matched by finding 22.02.6 [Major]: "no benchmark comparison with non-mechanistic models")

**Findings classification:**
- 22.02.1 [Major] Profile for beta is flat; CI not a valid confidence interval: B (matches Human Issue #1)
- 22.02.2 [Major] Profile methodology nonstandard — nuisance parameters not optimized at each fixed beta: A
- 22.02.3 [Major] No replicated particle filter evaluation — likelihood values come from mif2 internal output: A
- 22.02.4 [Major] Measurement model distribution never specified: A
- 22.02.5 [Major] Funeral exposure term likely violates conservation of susceptibles: A
- 22.02.6 [Major] No benchmark comparison with non-mechanistic models: B (matches Human Issue #8)
- 22.02.7 [Major] Parameter convergence absent for most parameters: A
- M1 [Minor] mu_EI parameter values biologically implausible (~1-2 hour incubation): C
- M2 [Minor] Population N for Sierra Leone inconsistent between text and trace plot: C
- M3 [Minor] Death rate fixed at 50% without citation or justification: C
- M4 [Minor] Conclusion about equal CIs is circular: D (matches Human Issue #3)
- M5 [Minor] Np and Nmif not reported in text: C
- M6 [Minor] All figures lack captions: D (matches Human Issue #7)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 8 | 12 | 6 | 5 |
| B (AI major, human also found) | 0 | 3 | 2 | 2 |
| C (AI minor, human missed) | 5 | 0 | 6 | 4 |
| D (AI minor, human also found) | 2 | 0 | 1 | 2 |
| E (Human found, AI missed) | 6 | 5 | 5 | 4 |

---

## Per-Reviewer Metrics

Human Recall = (B+D) / (B+D+E)
AI-Unique Rate = (A+C) / (A+B+C+D)

| Reviewer | B | D | E | Recall | A | C | AI-Unique Rate |
|----------|--:|--:|--:|-------:|--:|--:|---------------:|
| Alex | 0 | 2 | 6 | 2/8 = 25.0% | 8 | 5 | 13/15 = 86.7% |
| Charlie | 3 | 0 | 5 | 3/8 = 37.5% | 12 | 0 | 12/15 = 80.0% |
| Doug | 2 | 1 | 5 | 3/8 = 37.5% | 6 | 6 | 12/15 = 80.0% |
| Evan | 2 | 2 | 4 | 4/8 = 50.0% | 5 | 4 | 9/13 = 69.2% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #2: Evidence of a strong nonlinear relationship between Beta and eta.
- Human Issue #4: The weak identifiability might suggest exploring the possibility of fixing one or more parameters at scientifically plausible values.
- Human Issue #5: References at the end are not all cited when relevant during the main text.
- Human Issue #6: The connection to https://kingaa.github.io/sbied/ebola/ was not made explicit.

Count: 4 out of 8 human issues were missed by all reviewers (50%).

### Unique finds per reviewer

Human issues that only one reviewer covered and all others missed:

- Human Issue #7 (figure captions, numbers, section numbers): covered only by Evan (via M6).

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 1 |

### Universal AI-only flags

Issues raised by every reviewer that the human did not mention:

- Measurement model misspecification involving the accumulator H (all four reviewers flagged this in various forms: Alex finding 1, Charlie finding 1, Doug finding 3, Evan finding 22.02.4/22.02.5).
- No benchmark comparison (flagged by Charlie, Doug, Evan as major; Alex did not flag this — so this is NOT universal across all four).
- Sierra Leone population error: flagged by Alex (finding 2), Charlie (finding 10), Doug (finding 5), Evan (M2). All four flagged this. The human did not raise the population error.

Reviewing more carefully for issues that all four raised:

1. Measurement model misspecification / H accumulator issue: Alex finding 1, Charlie finding 1, Doug finding 3, Evan finding 22.02.4 — all four flagged some form of measurement model error not mentioned by the human.
2. Sierra Leone population error: Alex finding 2, Charlie finding 10, Doug finding 5, Evan M2 — all four raised this.

Count: 2 universal AI-only flags.
