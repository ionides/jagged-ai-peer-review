# Ned-Clean Analysis — W24 Project 10

---

## Human Issues

1. There is too much R output for a final report.
2. Plotting the flu simulations for the manually chosen parameters may be less relevant than simulations from the estimated maximum likelihood parameters — it would be nice to know if those fit better visually.
3. It would have been useful (and routine practice) to provide an ARMA benchmark.
4. Having found a decent model for flu, it would be worthwhile to discuss the fitted parameters; these should also have units, where applicable.
5. References should have titles, authors and dates, in a standard format such as APA; there should also be more citations in the text.
6. The connection between COVID-19 in an Asian country and influenza in US is quite weak; there are extensive differences between both the societies and the viruses, and it is not explained how these differences become a strength or a purpose of the project.
7. The initial values of latent state variables are fixed, not estimated; these choices need more discussion, since they could be critical to the modeling.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed

**Findings classification:**
- Finding 1 (dN_RS drawn from I not R in COVID step): A — critical bug in COVID process model
- Finding 2 (profile likelihood for mu_SV invalid): A — starting points grouped by rho, mu_SV not perturbed
- Finding 3 (flu model drops R-to-S loop): A — flu Csnippet omits dN_RS transition
- Finding 4 (no SEIR baseline model for comparison): A — no likelihood-ratio test between SEIRV and SEIR
- Finding 5 (N=1,000,000 unjustified for flu model): A — arbitrary population size with no justification
- Finding 6 (rw.sd very small, local search barely moves from hand-tuned point): A — convergence may be spurious
- Finding 7 (Np=1000 at evaluation but Np=5000 in mif2): A — inconsistent particle count undermines reported loglik
- Finding 8 (COVID "failure" without diagnostics): A — no quantitative measure of max loglik or null-model comparison
- Finding 9 (hard-coded local file paths): C — non-reproducible absolute paths on local machine
- Finding 10 (flu data from personal GitHub URL): C — unstable URL with undocumented provenance
- Finding 11 (only mu_SV profiled, no justification for choice): C — no uncertainty quantification for other parameters
- Finding 12 (90% CI without justification): C — non-standard level, no reason given
- Finding 13 (model/diagram include R-to-S but flu code omits it): C — mathematical inconsistency with flu implementation
- Finding 14 (no ESS or filter failure diagnostics): C — particle degeneracy not checked
- Finding 15 (rho upper bound = 1.0 with logit transform): C — logit(1) = +Inf, numerical instability risk

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "No non-mechanistic benchmark comparison")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed

**Findings classification:**
- Major Issue 1 (dN_RS drawn from I not R in COVID): A — critical coding bug in COVID process model
- Major Issue 2 (profile computed over rho not mu_SV): A — starting guesses grouped by rho, invalid CI
- Major Issue 3 (no non-mechanistic benchmark comparison): B — matches Human Issue #3
- Major Issue 4 (visual-only goodness-of-fit, no quantitative assessment): A — no AIC, no saturated model comparison
- Major Issue 5 (hard-coded absolute file paths): A — EDA figures cannot be reproduced
- Major Issue 6 (flu SEIRV omits R->S loop): A — mu_RS estimated but inactive in flu model
- Major Issue 7 (insufficient global search convergence evidence): A — no convergence traces shown for global search
- Major Issue 8 (rw.sd magnitudes and cooling fraction unjustified): A — local vs. global rw.sd dramatic and unexplained
- Minor: Duplicate reference numbers (refs 4 and 6 identical): C — reference list error
- Minor: Typographic errors ("Methodlogy", stray period): C — presentation errors
- Minor: N=1,000,000 unjustified for flu model: C — arbitrary population size
- Minor: mu_RS estimated but inactive in flu model: C — reporting invalid parameter estimate in table
- Minor: No sessionInfo/package version information: C — reproducibility gap
- Minor: Profile CI uses 90% level without justification: C — non-standard confidence level
- Minor: COVID model abandoned without attempting model improvement: C — no model modifications attempted

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "No model diagnostics — no comparison of filtering-distribution simulations to observed data")
- Human Issue #3: covered (matched by finding: "No benchmark comparison for either disease model")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed

**Findings classification:**
- Major Issue 1 (dN_RS bug in COVID Csnippet): A — wrong compartment draws break model conservation
- Major Issue 2 (flu Csnippet silently removes R→S): A — mu_RS has no effect on flu dynamics
- Major Issue 3 (profile mis-designed: guesses by rho not mu_SV): A — no coverage guarantee over mu_SV axis
- Major Issue 4 (profile CI threshold nonstandard and reference loglik incorrect): A — 90% level unjustified and reference loglik may be wrong
- Major Issue 5 (no benchmark comparison): B — matches Human Issue #3
- Major Issue 6 (no model diagnostics of any kind): B — matches Human Issue #2 (no simulation from fitted parameters vs. observed data)
- Major Issue 7 (no quantitative goodness-of-fit for COVID analysis): A — COVID terminated with only visual trace inspection
- Major Issue 8 (parameter identifiability not assessed for key parameters): A — no profiles for Beta, mu_EI, mu_IR
- Minor: Hard-coded absolute paths: C — non-reproducible paths
- Minor: N=1,000,000 unjustified: C — arbitrary effective population size
- Minor: COVID rw.sd equal to parameter starting values: C — extremely large perturbations likely contributed to convergence failure
- Minor: Global search mif2 chained with second mif2(Nmif=50) unexplained: C — purpose and effect undocumented
- Minor: mu_SV not in rw.sd in profile and not in partrans: C — question of whether mu_SV is correctly fixed
- Minor: 90% CI level not justified: C — non-standard level without motivation
- Minor: No sessionInfo/package version documentation: C — reproducibility gap
- Minor: Duplicate and inconsistent reference numbering: C — refs 4 and 6 identical, angle-bracket citation format non-standard
- Minor: Methodology section heading misspelling ("Methodlogy"): C — typographic error
- Minor: No out-of-sample evaluation or forecast: C — no projection discussion given stated public health motivation

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 10 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "24.10.5 — No fitted model overlay for flu data")
- Human Issue #3: covered (matched by finding: "24.10.6 — No benchmark comparison")
- Human Issue #4: covered (matched by finding: "24.10.10 — Parameter estimates not compared to literature")
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed

**Findings classification:**
- 24.10.1 (dN_RS drawn from wrong compartment): A — breaks SEIRV conservation; applies to COVID analysis
- 24.10.2 (profile likelihood for mu_SV invalid): A — guesses by rho, mu_SV not fixed to grid, CI unreliable
- 24.10.3 (loglik discrepancy: profile ~30 units better than global search): A — unexplained 30-unit improvement in profile run
- 24.10.4 (mu_RS effectively not estimated — flat at 0.1 throughout): A — excluded from rw.sd in local search and profile
- 24.10.5 (no fitted model overlay for flu data): B — matches Human Issue #2
- 24.10.6 (no benchmark comparison): B — matches Human Issue #3
- 24.10.7 (H accumulator reset not confirmed): A — if H not reset, all reported logliks are incorrect
- 24.10.8 (ACF argument for POMP logically inverted): C — quickly dropping ACF supports simple ARMA, not POMP
- 24.10.10 (parameter estimates not compared to literature): D — matches Human Issue #4
- 24.10.11 (V compartment absorbing, vaccine waning not modeled): C — analogous concern to R→S loop not addressed
- 24.10.12 (ESS not monitored during filtering): C — particle degeneracy not checked

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 3 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 8 | 7 | 6 | 5 |
| B (AI major, human also found) | 0 | 1 | 2 | 2 |
| C (AI minor, human missed) | 7 | 7 | 10 | 3 |
| D (AI minor, human also found) | 0 | 0 | 0 | 1 |
| E (Human found, AI missed) | 7 | 6 | 5 | 4 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

**Alex:**
- Human Recall = (B+D) / (B+D+E) = (0+0) / (0+0+7) = 0/7 = **0.00 (0%)**
- AI-Unique Rate = (A+C) / (A+B+C+D) = (8+7) / (8+0+7+0) = 15/15 = **1.00 (100%)**

**Charlie:**
- Human Recall = (B+D) / (B+D+E) = (1+0) / (1+0+6) = 1/7 = **0.14 (14%)**
- AI-Unique Rate = (A+C) / (A+B+C+D) = (7+7) / (7+1+7+0) = 14/15 = **0.93 (93%)**

**Doug:**
- Human Recall = (B+D) / (B+D+E) = (2+0) / (2+0+5) = 2/7 = **0.29 (29%)**
- AI-Unique Rate = (A+C) / (A+B+C+D) = (6+10) / (6+2+10+0) = 16/18 = **0.89 (89%)**

**Evan:**
- Human Recall = (B+D) / (B+D+E) = (2+1) / (2+1+4) = 3/7 = **0.43 (43%)**
- AI-Unique Rate = (A+C) / (A+B+C+D) = (5+3) / (5+2+3+1) = 8/11 = **0.73 (73%)**

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer (Alex, Charlie, Doug, Evan) failed to cover:

- Human Issue #1: Too much R output in the final report.
- Human Issue #5: References should have titles, authors, and dates in APA format; more citations needed in text.
- Human Issue #6: The connection between COVID-19 in Malaysia and flu in the US is weak and unexplained.
- Human Issue #7: Initial values of latent state variables are fixed and not estimated; need more discussion.

**4 out of 7 human issues were missed by all reviewers.**

### Unique finds per reviewer

Issues covered by exactly one reviewer (all others missed):

- Human Issue #3 (ARMA benchmark): covered by Charlie, Doug, Evan — not unique to any one reviewer (3 covered it)
- Human Issue #2 (MLE simulation not shown): covered by Doug and Evan — not unique
- Human Issue #4 (fitted parameters discussion with units): covered only by Evan

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 1 |

Evan alone covered Human Issue #4 (fitted parameters should be discussed with units).

### Universal AI-only flags

Issues raised as Major by every reviewer that the human did not mention:

- The critical bug in the COVID Csnippet where dN_RS is drawn from compartment I instead of R (raised as Major by Alex, Charlie, Doug, and Evan).
- The profile likelihood for mu_SV is not a valid profile — starting guesses grouped by rho, mu_SV not fixed to a grid (raised as Major by Alex, Charlie, Doug, and Evan).
- The flu model silently omits the R→S reinfection loop that motivates the SEIRV structure (raised as Major by Alex, Charlie, Doug; as Major by Evan via 24.10.4 which addresses mu_RS being ineffective).

**3 issues were flagged as Major by all four reviewers but not raised by the human.**
