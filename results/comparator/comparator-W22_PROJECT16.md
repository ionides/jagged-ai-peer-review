# Comparator Analysis — W22 Project 16

---

## Human Issues

1. The rationale for choosing Moscow (Russia) is unclear. The assertion that "we chose this data because it has recorded and updated the number of confirmed cases, number of deaths, and number of recovered cases daily" seems surprising since many locations have reported regularly. Russian data was notoriously problematic, with reporting likely influenced by political considerations that might conflict with public health.

2. The model has no measurement or process over-dispersion which might cause problems fitting to data. This could explain the observed difficulties with convergence of the optimization.

3. A benchmark (e.g., ARMA or iid negative binomial) would help see whether the mechanistic model has reasonable statistical fit.

4. The model is complex (which is technically impressive) but maybe a more problematic assumption is the static structure. A referee pointed out that various difficulties of modelling covid-19 lie in the fact that people getting exposed to the virus, being infected, and recovering from the disease is a dynamic process, and most factors influencing the transmission process change along with time, such as policy and variants. It might be helpful to have a time-varying part in the model when fitting the Covid-19 data. Even when fitting to just one wave of the pandemic, lockdowns and other social factors changed rapidly.

5. According to the figure of the confirmed cases, we could see there is a small peak before the 50 days. After being fluctuated around small values for a short time, the data increase to be stable for about 150 days. At the last 50 days, there is no obvious tread of decreasing cases. All these characteristics demonstrate that the time-invariant model could not depict the data quite well. Other results from local and global search also verify this inference.

6. The authors propose a complex model, and to make progress they fix many of the parameters. That could be problematic if one or more parameters are accidentally fixed in a way that disagrees with the data.

7. Math punctuation is erratic. Best to punctuate math as text. A period goes at the end of the last line of math, not on a blank line.

8. The arrow from A to Sy is surprising, and could be considered for deletion. Generally, the definition of asymptomatics is that they go down a route that does not lead to symptoms.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "No Model Comparison or Likelihood Benchmarks")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed

**Findings classification:**
- Finding 1 (SIR-CDR completely unexecuted): A — primary model never run, no particle filtering or fitting results produced
- Finding 2 (Sy updated twice, conflicting logic): A — double-counting of flows in SIR-CDR C snippet is a fundamental code bug
- Finding 3 (Sy omits dN_SyH subtraction in else branch): A — dN_SyH subtracted twice from Sy due to capacity constraint structure
- Finding 4 (Force-of-infection splits Beta incorrectly): A — two simultaneous binomial draws from same source compartment S inflates transmission
- Finding 5 (Measurement model for SIR-D doubly stochastic): A — using latent stochastic D directly as mu in dnbinom creates non-standard structure
- Finding 6 (Global search severely underpowered): A — only 20 starting points for a 4-dimensional search
- Finding 7 (Profile likelihood over misspecified range): A — profiled range [0.01, 0.95] excludes the observed optimum above 100
- Finding 8 (No model comparison or likelihood benchmarks): B — no baseline comparison or null model log-likelihood (matches Human Issue #3)
- Finding 9 (eta value discrepancy between text and code): A — text states 0.002, code sets 0.0002
- Finding 10 (Mu_SyR renamed from Mu_R without explanation): C — parameter renamed between models with self-contradictory text
- Finding 11 (Equation 169 repeats dN_SyH): C — LaTeX transcription error gives two different definitions for same label
- Finding 12 (Capacity constraint C code bug): C — Sy + H - Cap evaluates incorrectly after H is already set to Cap
- Finding 13 (Population mismatch between data and parameters): C — model uses N = 11,920,000 while dataset reports 12,692,466
- Finding 14 (No ESS diagnostic plots): C — no effective sample size plots shown for any particle filter run
- Finding 15 (Conclusion overstates unexecuted model): C — no empirical basis for claiming SIR-CDR model is "worth reporting"

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "No comparison to any non-mechanistic benchmark")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "Fixed parameters are not justified with sensitivity analysis")
- Human Issue #7: missed
- Human Issue #8: missed

**Findings classification:**
- Finding 1 (SIR-CDR never fitted): A — primary model is set to eval=FALSE and never executed
- Finding 2 (Conservation violation in SIR-CDR rprocess): A — Sy compartment updated inconsistently, double-decrement possible
- Finding 3 (Duplicated dN_SyH label in equations): A — copy-paste error causes model/code mismatch
- Finding 4 (Profile likelihood is a slice): A — profile range excludes the MLE region, confidence intervals invalid
- Finding 5 (No non-mechanistic benchmark): B — no ARIMA, IID negative binomial, or other reference model (matches Human Issue #3)
- Finding 6 (No convergence diagnostics): A — global search spans 15,000 log-units indicating non-convergence, not adequately addressed
- Finding 7 (Fixed parameters not justified): B — Alpha, eta, D_rate fixed without sensitivity analysis, may mask misspecification (matches Human Issue #6)
- Finding 8 (SIR-D clamping code bug): A — after Sy=0, nearbyint(Sy*ratio) always returns 0, silent incorrect dynamics
- Finding 9 (SIR-CDR dmeas additive log-likelihoods): C — implementation is valid though unconventional; potential underflow risk
- Finding 10 (D_rate conflated with competing hazard): C — death rate parametrized as fraction of recovery rate, breaks at large Mu_SyR
- Finding 11 (Profile threshold uses incorrect reference loglik): C — Wilks threshold drawn at global MLE, not profile peak
- Finding 12 (run_level=2 with few replicates): C — only 10 profile points and 4 replicates over wrong parameter range
- Finding 13 (No simulation-based diagnostics): C — no conditional log-likelihood plot or filtering ESS analysis
- Finding 14 (Misspelled "miss-specified"): C — consistent typographical error across multiple sections
- Finding 15 (No sessionInfo() or package versions): C — no reproducibility documentation for pomp version used

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "No non-mechanistic benchmark comparison")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "Fixed parameters not estimated or given profile likelihoods")
- Human Issue #7: missed
- Human Issue #8: missed

**Findings classification:**
- Major Issue 1 (SIR-CDR accumulator double-counts C and Rr via shared rho*dN_SyR flow): A — double-counting in measurement accumulators
- Major Issue 2 (dN_SyH defined twice with different rates — notation error): A — equation mislabeling in process model
- Major Issue 3 (capacity mechanism zeroes Sy compartment, violates conservation): A — compartment conservation bug in overflow branch
- Major Issue 4 (global IF2 search initialized from previous mif2 result, inheriting stale cooling schedule): A — global search initialization error
- Major Issue 5 (profile likelihood grid [0.01, 0.95] excludes global MLE near 100): A — profile range misalignment
- Major Issue 6 (no non-mechanistic benchmark comparison): B — no benchmark model (matches Human Issue #3)
- Major Issue 7 (no log-likelihood or goodness-of-fit reported for SIR-CDR model): A — missing quantitative fit metric
- Major Issue 8 (substantive conclusions drawn from self-diagnosed non-converged results): A — conclusions unsupported by non-converged optimization
- Major Issue 9 (SIR-D overflow branch uses stale Sy=0 value, R and D receive no flow): A — stale variable bug in overflow branch
- Minor: Mu_SyR absent from paramnames but named in text: C — text-code mismatch on parameter identity
- Minor: partrans declared in both pomp() and mif2() calls: C — duplicate transformation specification
- Minor: fixed parameters Alpha and D_rate have no sensitivity analysis or profile likelihoods: D — fixed parameters not evaluated (matches Human Issue #6)
- Minor: run_level=2 uses only 1000 particles, too low for 5-compartment model: C — insufficient particle count
- Minor: no simulation envelope shown around trajectory comparison: C — missing predictive envelope
- Minor: conclusion misstates paper's primary contribution: C — framing inconsistent with results

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "22.16.D — SIR-CDR measurement model uses Poisson, lacking overdispersion, causing ESS collapse")
- Human Issue #3: covered (matched by finding: "22.16.C — no benchmark comparison against non-mechanistic baseline")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "22.16.G — overdispersion parameter k not perturbed in local search, effectively fixed without justification")
- Human Issue #7: missed
- Human Issue #8: missed

**Findings classification:**
- 22.16.A: A — process model error in dN_SyD couples death hazard to recovery rate, driving implausible Mu_SyR estimate
- 22.16.B: A — profile likelihood range [0,1] entirely excludes the MLE found in global search (~54–228)
- 22.16.C: B — no benchmark comparison against ARIMA or negative binomial baseline (matches Human Issue #3)
- 22.16.D: B — SIR-CDR measurement model uses underdispersed Poisson; overdispersion needed (matches Human Issue #2)
- 22.16.E: A — sequential independent binomial draws from shared compartments violate conservation; multinomial step required
- 22.16.F: C — Cap parameter appears in description but not in parameter list or optimization results
- 22.16.G: D — overdispersion parameter k held flat throughout local search, not optimized (matches Human Issue #6)
- 22.16.H: C — ~20-unit spread among nominally converged global search runs suggests flat likelihood or high Monte Carlo noise
- 22.16.I: C — dN_SyH appears twice in SIR-CDR equations; dN_SyD was likely intended on the second occurrence
- 22.16.J: C — no ESS trace shown for SIR-D model to distinguish computational inadequacy from model misspecification

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 8 | 6 | 8 | 3 |
| B (AI major, human also found) | 1 | 2 | 1 | 2 |
| C (AI minor, human missed) | 6 | 7 | 5 | 4 |
| D (AI minor, human also found) | 0 | 0 | 1 | 1 |
| E (Human found, AI missed) | 7 | 6 | 6 | 5 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 1 | 0 | 7 | 1/8 = 12% | 8 | 6 | 14/15 = 93% |
| Charlie | 2 | 0 | 6 | 2/8 = 25% | 6 | 7 | 13/15 = 87% |
| Doug | 1 | 1 | 6 | 2/8 = 25% | 8 | 5 | 13/15 = 87% |
| Evan | 2 | 1 | 5 | 3/8 = 38% | 3 | 4 | 7/10 = 70% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #1: The rationale for choosing Moscow (Russia) is unclear. The assertion that "we chose this data because it has recorded and updated the number of confirmed cases, number of deaths, and number of recovered cases daily" seems surprising since many locations have reported regularly. Russian data was notoriously problematic, with reporting likely influenced by political considerations that might conflict with public health. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #4: The model is complex (which is technically impressive) but maybe a more problematic assumption is the static structure. A referee pointed out that various difficulties of modelling covid-19 lie in the fact that people getting exposed to the virus, being infected, and recovering from the disease is a dynamic process, and most factors influencing the transmission process change along with time, such as policy and variants. It might be helpful to have a time-varying part in the model when fitting the Covid-19 data. Even when fitting to just one wave of the pandemic, lockdowns and other social factors changed rapidly. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #5: According to the figure of the confirmed cases, we could see there is a small peak before the 50 days. After being fluctuated around small values for a short time, the data increase to be stable for about 150 days. At the last 50 days, there is no obvious tread of decreasing cases. All these characteristics demonstrate that the time-invariant model could not depict the data quite well. Other results from local and global search also verify this inference. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #7: Math punctuation is erratic. Best to punctuate math as text. A period goes at the end of the last line of math, not on a blank line. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #8: The arrow from A to Sy is surprising, and could be considered for deletion. Generally, the definition of asymptomatics is that they go down a route that does not lead to symptoms. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 5 out of 8 human issues (62%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #2: The model has no measurement or process over-dispersion which might cause problems fitting to data. This could explain the observed difficulties with convergence of the optimization. (Covered only by Evan)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 1 |
