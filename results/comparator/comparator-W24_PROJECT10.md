# Comparator Analysis — W24 Project 10

---

## Human Issues

1. There is too much R output for a final report.

2. Plotting the flu simulations for the manually chosen parameters may be less relevant for the final results than simulations from the estimated maximum likelihood parameters. It would be nice to know if those fit better, visually.

3. It would have been useful (and routine practice) to provide an ARMA benchmark. This project properly focuses primarily on interpretable mechanistic models, but a brief excursion into ARMA modeling would be helpful.

4. Having found a decent model for flu, it would be worthwhile to discuss the fitted parameters. These should also have units, where applicable.

5. References should have titles, authors and dates, in a standard format such as APA. There should also be more citations in the text.

6. The connection between COVID-19 in an Asian country and influenza in US is quite weak; there are extensive differences between both the societies and the viruses. It is not explained how these differences become a strength or a purpose of the project.

7. The initial values of latent state variables are fixed, not estimated. These choices need more discussion, since they could be critical to the modeling.

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
- Finding 1 (dN_RS drawn from I instead of R — COVID bug): A — critical coding error in COVID step function, no matching human issue
- Finding 2 (profile likelihood for mu_SV is not a valid profile): A — invalid profile likelihood construction, no matching human issue
- Finding 3 (flu model drops R-to-S reinfection loop): A — flu model is SEIV not SEIRV as described, no matching human issue
- Finding 4 (no no-vaccination baseline model): A — no SEIR baseline fitted for comparison, no matching human issue
- Finding 5 (N = 1,000,000 unjustified): A — arbitrary population size with no justification, no matching human issue
- Finding 6 (local search rw.sd values extremely small, hand-tuned start): A — spurious convergence from hand-tuned initial point, no matching human issue
- Finding 7 (Np = 1000 at evaluation vs Np = 5000 in mif2): A — inconsistent particle count undermines log-likelihood estimates, no matching human issue
- Finding 8 (COVID "failure" without rigorous diagnostics): A — qualitative failure conclusion without quantitative support, no matching human issue
- Finding 9 (hard-coded absolute file paths): C — reproducibility issue with local paths, no matching human issue
- Finding 10 (flu data loaded from personal GitHub URL): C — unstable data provenance, no matching human issue
- Finding 11 (only one parameter profiled, selection unjustified): C — limited uncertainty quantification, no matching human issue
- Finding 12 (90% CI level without justification): C — non-standard confidence level unjustified, no matching human issue
- Finding 13 (diagram and equations include R-to-S but flu code omits it): C — mathematical description inconsistent with flu implementation, no matching human issue
- Finding 14 (no ESS or filter failure diagnostics): C — particle filter diagnostics absent, no matching human issue
- Finding 15 (rho upper bound = 1.0 with logit transform): C — numerical instability risk, no matching human issue

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
- Human Issue #2: covered (matched by finding: "no simulation-based diagnostic using MLE parameters; simulation plot uses manually chosen parameter set")
- Human Issue #3: covered (matched by finding: "no benchmark comparison — neither COVID nor flu analysis includes a non-mechanistic benchmark")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed

**Findings classification:**
- Major Issue 1 (COVID rprocess R→S draws from I instead of R): A — critical implementation bug causing COVID model to differ from stated equations
- Major Issue 2 (flu rprocess omits R→S transition entirely): A — flu model effectively SEIV with absorbing R, not SEIRV as described
- Major Issue 3 (profile likelihood for mu_SV not correctly constructed): A — starting guesses grouped by rho not mu_SV; mu_SV not fixed on a grid
- Major Issue 4 (no benchmark comparison): B — no ARMA or other non-mechanistic benchmark for either dataset (matches Human Issue #3)
- Major Issue 5 (COVID rw.sd values equal parameter values, ~100x too large): A — perturbation sizes cause random walk rather than directed optimization
- Major Issue 6 (COVID analysis abandoned without model revision): A — no global search or alternative structures attempted after convergence failure
- Minor (EDA vs POMP data source inconsistency): C — flu data loaded from local path in EDA and GitHub URL in POMP section
- Minor (global search rw.sd ~10x too small for flu): C — may over-rely on starting values
- Minor (mu_RS estimated but inactive in flu model): C — inactive parameter consumes degrees of freedom without effect
- Minor (profile uses 90% CI without justification): C — non-standard level not explained
- Minor (duplicate reference entries 4 and 6): C — identical CDC URL cited twice
- Minor (N=1,000,000 population size not justified): C — does not represent US population or defined catchment area
- Minor (simulation uses manually chosen parameters not MLE): D — flu simulation plot uses manually chosen Beta=10 etc. rather than fitted MLE (matches Human Issue #2)
- Minor (Section 5 title proposes structural explanations but failure partly implementation artifact): C — failure may be due to code bugs and wrong rw.sd rather than fundamental model limitation
- Minor (typographical errors): C — "Methodlogy," "Intepretation," "serach"

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "No model diagnostics — single forward-simulation at fixed parameter values is insufficient; filtering-distribution simulations to observed data are absent")
- Human Issue #3: covered (matched by finding: "No benchmark comparison for either disease model")
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "Duplicate and inconsistent reference numbering; non-standard citation format")
- Human Issue #6: missed
- Human Issue #7: missed

**Findings classification:**
- Major 1 (COVID Csnippet bug: R→S draws from I instead of R): A — foundational code error in COVID waning-immunity transition
- Major 2 (Flu Csnippet silently removes R→S transition): A — mu_RS has no effect on flu model dynamics
- Major 3 (Profile likelihood mis-designed: starting guesses grouped by rho not mu_SV): A — profile coverage over mu_SV axis is not guaranteed
- Major 4 (Profile CI threshold nonstandard and inconsistently applied): A — 90% CI used without justification; reference likelihood may be wrong
- Major 5 (No benchmark comparison for either disease model): B — matches Human Issue #3
- Major 6 (No model diagnostics of any kind): B — matches Human Issue #2
- Major 7 (No quantitative goodness-of-fit reported for COVID analysis): A — only trace plots used to conclude model failure
- Major 8 (Parameter identifiability not assessed for key parameters): A — no profile likelihoods computed for Beta, mu_EI, mu_IR
- Minor (Hard-coded absolute paths): C — local file paths will break rendering on other systems
- Minor (Flu population size N=1,000,000 unjustified): C — scaling assumption for Beta is unexplained
- Minor (COVID local search rw.sd values equal to parameter starting values): C — extremely large perturbations not discussed
- Minor (Global search mif2 chained with second mif2 refinement): C — chaining rationale and cooling schedule effect undocumented
- Minor (Profile search mu_SV absent from rw.sd): C — whether mu_SV is correctly fixed at guess value is unverified
- Minor (90% CI level not justified): C — deviation from standard 95% is unmotivated
- Minor (No sessionInfo or package version documentation): C — reproducibility compromised across pomp versions
- Minor (Duplicate and inconsistent reference numbering): D — matches Human Issue #5
- Minor (Methodology section heading misspelling "Methodlogy"): C — typographical error in section heading
- Minor (No out-of-sample evaluation or forecast): C — no projection or forecast given stated public-health motivation

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "24.10.5 — no fitted model overlay for flu data")
- Human Issue #3: covered (matched by finding: "24.10.6 — no benchmark comparison")
- Human Issue #4: covered (matched by finding: "24.10.10 — parameter estimates not compared to literature")
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed

**Findings classification:**
- 24.10.1: A — code bug: dN_RS drawn from Infectious (I) instead of Recovered (R) compartment
- 24.10.2: A — profile likelihood for mu_SV is not a valid profile; CI is invalid
- 24.10.3: A — unexplained 30-unit loglik discrepancy between profile scatter and global search
- 24.10.4: A — mu_RS is effectively not estimated; fixed at 0.1/week without justification
- 24.10.5: B — no fitted model overlay for flu data (matches Human Issue #2)
- 24.10.6: B — no benchmark comparison against a non-mechanistic baseline (matches Human Issue #3)
- 24.10.7: A — H accumulator reset not confirmed; may produce cumulative rather than interval likelihoods
- 24.10.8: C — ACF argument for needing POMP is logically inverted
- 24.10.10: D — parameter estimates not compared to literature or given contextual discussion (matches Human Issue #4)
- 24.10.11: C — V compartment is absorbing; vaccine waning not modeled or acknowledged
- 24.10.12: C — effective sample size not monitored during particle filtering

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
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 8 | 5 | 6 | 5 |
| B (AI major, human also found) | 0 | 1 | 2 | 2 |
| C (AI minor, human missed) | 7 | 8 | 9 | 3 |
| D (AI minor, human also found) | 0 | 1 | 1 | 1 |
| E (Human found, AI missed) | 7 | 5 | 4 | 4 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 0 | 0 | 7 | 0/7 = 0% | 8 | 7 | 15/15 = 100% |
| Charlie | 1 | 1 | 5 | 2/7 = 29% | 5 | 8 | 13/15 = 87% |
| Doug | 2 | 1 | 4 | 3/7 = 43% | 6 | 9 | 15/18 = 83% |
| Evan | 2 | 1 | 4 | 3/7 = 43% | 5 | 3 | 8/11 = 73% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #1: There is too much R output for a final report. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #6: The connection between COVID-19 in an Asian country and influenza in US is quite weak; there are extensive differences between both the societies and the viruses. It is not explained how these differences become a strength or a purpose of the project. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #7: The initial values of latent state variables are fixed, not estimated. These choices need more discussion, since they could be critical to the modeling. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 3 out of 7 human issues (43%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #4: Having found a decent model for flu, it would be worthwhile to discuss the fitted parameters. These should also have units, where applicable. (Covered only by Evan)
- Human Issue #5: References should have titles, authors and dates, in a standard format such as APA. There should also be more citations in the text. (Covered only by Doug)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 1 |
| Evan | 1 |
