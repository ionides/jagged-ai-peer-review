# Comparator Analysis — W21 Project 02

---

## Human Issues

1. None of the models under consideration can capture the multiple waves evident from the data. The first wave might have been brought under control by lockdown interventions, whose end led to the second wave. The third wave might be partly due to the end of distancing interventions used for the second wave, partly due to new strains. None of these things can be represented in the models used - quantitative understanding of the COVID waves may require additional modeling detail. Modeling multiple COVID waves is not easy: see Projects 13 & 15 for successful approaches.

2. Please explain what the "infected" variable measures. Is it the number of positive tests? Does this raise issues for understanding the data?

3. The project support a claim that "It is impossible to use SEIR, SEIQR and SECSDR to simulate the daily Infected case no matter how to change the parameters" but it is possible to make appropriate modifications to allow these models to fit the data. The key question becomes what modification(s) are needed. In the conclusion, the project notes that time-varying parameters could be the key for doing this. Retrospectively, the authors might have tried to hypothesize how adding extra Q, C, D compartments will fix the problem before spending time on these model variations.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "SEIQR measurement model links Q to observed infections, not new diagnoses — observed daily confirmed cases are new positive tests, not a stock")
- Human Issue #3: missed

**Findings classification:**
- Finding 1 (SEIR degenerate normal dmeas): A — SEIR dmeas sets sd = mean, rendering tau a phantom parameter
- Finding 2 (SECSDR double-deduction from Ca): A — illegal sequential binomial draws violate population conservation
- Finding 3 (SEIQR links Q stock to observed flow): B — observed infections are new positive tests, not currently quarantined individuals; stock/flow confusion (matches Human Issue #2)
- Finding 4 (cooling fraction/RW SD near zero): A — mif2 optimizer cannot explore parameter space for SECSDR and SEIQR
- Finding 5 (SEIQR N = 32M not 328M): A — population parameter is one-tenth the US population with no justification
- Finding 6 (no local search for SECSDR/SEIQR): A — no convergence diagnostic for two of three models
- Finding 7 (no likelihood comparison across models): A — conclusions rely on visual inspection, no log-likelihood or AIC table
- Finding 8 (data file missing): A — blinded.Rmd reads a CSV not present in directory; reproducibility broken
- Finding 9 (SEIR local search omits mu_EI and mu_IR): C — rate parameters fixed during local search, MLE unlikely reached
- Finding 10 (hard-coded simulation parameters): C — parameters embedded as literals rather than extracted from saved results object
- Finding 11 (dmeas/rmeas distribution mismatch): C — dmeas uses sd = rho*H, rmeas uses sd = sqrt(rho*H); inconsistent particle weighting
- Finding 12 (run_level=1 for SECSDR): C — only 10 mif2 iterations and 100 particles; pilot-level, not publishable
- Finding 13 (SECSDR hard-coded rinit): C — initial susceptible fraction fixed, optimizer cannot adjust it over year-long series
- Finding 14 (no profile likelihood or CIs): C — parameter identifiability unassessed for all three models
- Finding 15 (no quantitative epidemiological motivation): C — introduction cites no literature values for R0, incubation period, or infectious period

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "No discussion of measurement model's biological meaning — H tracks cumulative recoveries but recovery=diagnosis is unstated")
- Human Issue #3: covered (matched by finding: "Catastrophically misconfigured iterated filtering — conclusion that models fail is not attributable to model misspecification")

**Findings classification:**
- Finding 1 (Misconfigured iterated filtering): B — catastrophically misconfigured mif2 for SECSDR and SEIQR means conclusion that models fail cannot be attributed to model misspecification (matches Human Issue #3)
- Finding 2 (Missing data file): A — data file absent from submission, preventing reproducibility
- Finding 3 (No non-mechanistic benchmark): A — no ARMA/ARIMA or other baseline for quantitative comparison
- Finding 4 (SEIR measurement model misspecified): A — zero variance when H=0 causes degenerate likelihood evaluations
- Finding 5 (SECSDR conservation violated): A — S decremented by dN_ECa rather than dN_SE, individuals disappear from population
- Finding 6 (No profile likelihood or CIs): A — no uncertainty quantification for any parameter in any model
- Finding 7 (SEIR local search excludes parameters): A — mu_EI, mu_IR, tau not perturbed during local search
- Finding 8 (Global search without re-specifying rw.sd): A — SEIR global search inherits local search perturbation magnitudes
- Finding 9 (SEIQR population size wrong): A — N fixed at 32,000,000 instead of U.S. population of 300,000,000
- Finding 10 (No convergence diagnostics): A — trace plots shown but convergence not demonstrated or discussed for any model
- Finding 11 (SECSDR/SEIQR run_level too low): A — SECSDR uses run_level=1 (debugging-level computation)
- Finding 12 (No ARIMA or classical time series analysis): C — no preliminary ACF/PACF or ARMA analysis before mechanistic modeling
- Finding 13 (Hard-coded simulation parameters): C — best parameters hard-coded rather than extracted programmatically from optimization output
- Finding 14 (No discussion of measurement model's biological meaning): D — SEIR accumulator H represents cumulative recoveries, but whether recovery equals diagnosis is unstated; SEIQR uses quarantine compartment Q without epidemiological justification (matches Human Issue #2)
- Finding 15 (References incomplete): C — no epidemiological literature or POMP methodology references cited

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 10 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 3 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 1 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed

**Findings classification:**
- Major 1 (negligible rw.sd renders IF2 inoperative for SECSDR and SEIQR): A — IF2 optimization is inoperative because rw.sd = 2e-9 is 4–8 orders of magnitude too small and cooling.fraction.50 = 0.00005 reduces perturbations below machine epsilon
- Major 2 (SEIR dmeasure variance equals mean-squared rather than mean): A — dmeasure uses sd = |mean| while rmeasure uses sd = sqrt(mean), so the two snippets implement different variance functions
- Major 3 (SEIQR population size is 32,000,000 instead of 328,000,000): A — N is a factor of 10 too small, inflating per-capita transmission rate and making SEIQR estimates irreconcilable with other models
- Major 4 (no benchmark comparison against a non-mechanistic model): A — no ARIMA or auto-regressive baseline is fitted, so there is no reference point for the mechanistic models' quantitative fit
- Major 5 (no profile likelihoods; parameter identifiability not assessed): A — neither profile likelihoods nor confidence intervals are computed for any parameter of any model
- Major 6 (no quantitative goodness-of-fit or model comparison): A — no log-likelihood values for SEIR are reported after optimization and no AIC or cross-model comparison is presented
- Major 7 (SECSDR rprocess compartment depletion accounting error): A — dN_ECa arrivals to Ca are not added before computing competing-risk draws, distorting flows out of Ca
- Major 8 (inconsistent run_level settings across models): A — SECSDR uses run_level=1 (Np=100, Nmif=10) while SEIQR uses run_level=2 (Np=2000, Nmif=100), making cross-model log-likelihood comparisons invalid
- Major 9 (no model diagnostics — ESS, conditional log-likelihoods, filtering distribution): A — no conditional log-likelihood plots, ESS traces, or filtering-distribution comparisons are presented for any model
- Major 10 (SECSDR rinit missing E compartment; latency collapsed): A — E is absent from statenames and individuals move directly from S to Ca, collapsing the latency compartment without acknowledgment
- Minor (ungrammatical URL in introduction): C — URL is embedded in running text with curly braces rather than formatted as a hyperlink or footnote
- Minor (orphan tau parameter declared but unused in any Csnippet): C — tau appears in paramnames and partrans but not in seir_step, dmeas, or rmeas
- Minor (SEIR global search anchored near local-search solution): C — global search passes a previous mif2 result as first argument, inheriting the cooling schedule and anchoring near the local solution
- Minor (SEIQR uses Q stock as observation mean rather than a daily-incidence flow): C — dmeasure uses Q (cumulative quarantined individuals) as mean of observation distribution without an accumulator or differencing
- Minor (simulated results use second-best rather than best parameter set): C — para is taken from the replicate ranked second in log-likelihood with no justification
- Minor (conclusion discusses temporal phase decomposition speculatively with no analysis): C — future work on dividing 400 days into phases is discussed without any supporting preliminary analysis
- Minor (reference list cites only student projects, no peer-reviewed literature): C — references [2] and [3] are other student projects; no peer-reviewed epidemiological or statistical methods paper is cited
- Minor (tau plotted in SEIR local-search trace panels despite not being updated by IF2): C — tau is plotted as a convergence trace even though it has no rw.sd argument and is never moved by IF2

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 10 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "21.02.m4 — data description incomplete; 'Infected' variable undefined")
- Human Issue #3: missed

**Findings classification:**
- 21.02.1: A — inconsistent measurement model in SEIR (dmeas/rmeas mismatch)
- 21.02.2: A — phantom parameter tau declared but never used in SEIR
- 21.02.3: A — E compartment absent from SECSDR statenames and rinit
- 21.02.4: A — SEIQR population size N=32,000,000 inconsistent with US scale
- 21.02.5: A — rho used as noise scale rather than reporting fraction in SECSDR and SEIQR
- 21.02.6: A — no non-mechanistic benchmark for comparison
- 21.02.7: A — numerically absurd log-likelihood values (~-1e14) in SEIQR diagnostics
- 21.02.8: A — no profile likelihoods or confidence intervals reported
- 21.02.m1: C — Np and Nmif not reported for any model
- 21.02.m2: C — SECSDR rinit inconsistency due to missing E compartment
- 21.02.m3: C — no EDA or preliminary time-series analysis of multi-wave structure
- 21.02.m4: D — data description incomplete; "Infected" variable not defined (matches Human Issue #2)
- 21.02.m5: C — reference list minimal; no primary COVID-19 modeling literature cited

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 7 | 10 | 10 | 8 |
| B (AI major, human also found) | 1 | 1 | 0 | 0 |
| C (AI minor, human missed) | 7 | 3 | 8 | 4 |
| D (AI minor, human also found) | 0 | 1 | 0 | 1 |
| E (Human found, AI missed) | 2 | 1 | 3 | 2 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 1 | 0 | 2 | 1/3 = 33% | 7 | 7 | 14/15 = 93% |
| Charlie | 1 | 1 | 1 | 2/3 = 67% | 10 | 3 | 13/15 = 87% |
| Doug | 0 | 0 | 3 | 0/3 = 0% | 10 | 8 | 18/18 = 100% |
| Evan | 0 | 1 | 2 | 1/3 = 33% | 8 | 4 | 12/13 = 92% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #1: None of the models under consideration can capture the multiple waves evident from the data. The first wave might have been brought under control by lockdown interventions, whose end led to the second wave. The third wave might be partly due to the end of distancing interventions used for the second wave, partly due to new strains. None of these things can be represented in the models used - quantitative understanding of the COVID waves may require additional modeling detail. Modeling multiple COVID waves is not easy: see Projects 13 & 15 for successful approaches. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 1 out of 3 human issues (33%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #3: The project support a claim that "It is impossible to use SEIR, SEIQR and SECSDR to simulate the daily Infected case no matter how to change the parameters" but it is possible to make appropriate modifications to allow these models to fit the data. The key question becomes what modification(s) are needed. In the conclusion, the project notes that time-varying parameters could be the key for doing this. Retrospectively, the authors might have tried to hypothesize how adding extra Q, C, D compartments will fix the problem before spending time on these model variations. (Covered only by Charlie)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 1 |
| Doug | 0 |
| Evan | 0 |
