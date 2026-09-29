# Comparator Analysis — W22 Project 20

---

## Human Issues

1. For exploratory data analysis and/or ARMA and/or wavelets, it might be worth looking at the logarithm of the data since population dynamics are usually closer to linear on a log scale.

2. For whatever reason, the noise on your maximization is quite large (many log units) so the crude cutoff of 1.92 log units on the profile is primarily noise. One could use a smoothed estimate of the likelihood to improve this somewhat.

3. The use of Box-Cox transformations for ARMA models is not explained, and exactly what was done is unclear. Are ARMA likelihoods properly adjusted for a transformation?

4. What is the purpose of fitting the SARMA model to a different time interval from the mechanistic data - in that case, it no longer provides a benchmark likelihood.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "Degenerate Profile Likelihood Confidence Intervals — single-point CIs indicate the profile likelihood is too flat/noisy to yield valid intervals")
- Human Issue #3: covered (matched by finding: "BoxCox Transformation Is Applied to Shifted Data With Arbitrary Constant — transformation not justified or explained")
- Human Issue #4: covered (matched by finding: "Incomparable Likelihoods Between SARIMA and SIRS Models — different time windows and transformations make the benchmark comparison invalid")

**Findings classification:**
- Finding 1 (Critical Bug: Profile Trace for `b` Groups by `a`): A — coding error causing misleading profile trace visualization
- Finding 2 (Degenerate Profile Likelihood CIs): B — single-point CIs indicate the profile is too flat/noisy to yield valid intervals (matches Human Issue #2)
- Finding 3 (sin vs. cos Inconsistency in Seasonality Model): A — equation in text uses cosine but code uses sine, documentation error
- Finding 4 (Null Hypothesis Test Not Executed): A — core scientific question of whether b < a is never formally tested
- Finding 5 (Very Poor Final POMP Likelihood Despite Run Level 3): A — wide likelihood range and lack of convergence undermine the optimization
- Finding 6 (Local Search Uses Sequential `%do%` Instead of Parallel `%dopar%`): A — missed parallelization opportunity in local search
- Finding 7 (Incomparable Likelihoods Between SARIMA and SIRS Models): B — different time windows, transformations, and data subsets make the benchmark comparison methodologically invalid (matches Human Issue #4)
- Finding 8 (Measurement Model Returns `lik = 0` for Boundary Cases): A — dmeasure returns 0 instead of -Inf under give_log, corrupting the particle filter
- Finding 9 (Section 4.4 Is Missing): A — section numbering skips 4.4 with no explanation
- Finding 10 (BoxCox Transformation Applied With Arbitrary Constant): D — Box-Cox constant 1050 is unjustified and the transformation is not explained (matches Human Issue #3)
- Finding 11 (SARIMA Fit and Prediction Data Subsets Described Inaccurately): C — start dates for forecasting plots are unexplained in the text
- Finding 12 (rho Fixed at Imprecisely Justified Value): C — arithmetic justification for rho = 4e-5 is inconsistent and the value is never searched over
- Finding 13 (Global Search Dispersion Appears Unreliable): C — biologically implausible parameter values in global search results go uncommented
- Finding 14 (Missing Convergence Diagnostics for Global Search): C — no mif2 convergence traces shown for global search
- Finding 15 (Wavelet Section Adds Little Value, Contains Minor Error): C — integration variable inconsistency in wavelet formula; result is redundant with simpler tools

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 1 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by findings: "Profile likelihoods are degenerate: CIs collapse to single points" and "Global search box computed from full likelihood table including implausible values")
- Human Issue #3: covered (matched by finding: "BoxCox transformation introduces an arbitrary offset (+1050) with no justification")
- Human Issue #4: covered (matched by finding: "SARIMA and POMP likelihoods applied to different datasets and cannot support benchmark comparison")

**Findings classification:**
- Finding 1 (measurement model returns 0 instead of -Inf for invalid states): A — coding error silently corrupts particle filter weights
- Finding 2 (cos in writeup vs sin in code): A — mathematical model contradicts code implementation
- Finding 3 (POMP log-likelihood three orders of magnitude below SARIMA): A — magnitude gap signals fundamental misspecification but benchmark not meaningful
- Finding 4 (profile likelihoods degenerate, CIs collapse to single points): B — noisy/sparse profile makes CI claims invalid (matches Human Issue #2)
- Finding 5 (rho fixed at implausibly small value, mu_IR biologically implausible): A — unjustified fixed reporting rate with compensating parameter confound
- Finding 6 (local search uses %do% instead of %dopar%): A — sequential execution inconsistent with intended parallel design
- Finding 7 (global search box derived from full table including implausible values): B — wide box yields profile failures explaining degenerate CIs (matches Human Issue #2)
- Finding 8 (missing convergence diagnostics for global search): A — no trace plots; local search acknowledged not to have converged
- Finding 9 (SARIMA and POMP on different datasets, benchmark comparison invalid): B — different time windows and scales mean likelihoods are not comparable (matches Human Issue #4)
- Finding 10 (AIC table values are per-observation normalized, not standard scale): C — normalization undisclosed, adds to cross-model confusion
- Finding 11 (rho in partrans but in fixed_params): C — inconsistent specification, transformation defined but unused
- Finding 12 (BoxCox offset +1050 unjustified): D — arbitrary constant offset unexplained, transformation properties unclear (matches Human Issue #3)
- Finding 13 (SARIMA prediction description inaccurate): C — training window stated as through 2018 but actually ends mid-2018
- Finding 14 (no model diagnostics beyond visual simulation for SIRS): C — no conditional log-likelihoods or ESS analysis shown
- Finding 15 (pandemic cutoff hardcoded as week 260, not documented): C — fragile hardcoded threshold absent from mathematical writeup

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 1 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by findings: "Major Issue 2 — profile curves unreliable due to inherited cooled IF2 base object" and "Major Issue 4 — sparse/scattered profile CI point clouds consistent with insufficient computational effort")
- Human Issue #3: covered (matched by finding: "Minor — BoxCox transformation hardcoded shift not explained")
- Human Issue #4: covered (matched by findings: "Major Issue 3 — SARIMA fitted to different time interval, making log-likelihood comparison invalid" and "Major Issue 5 — no valid benchmark because models fitted to different datasets")

**Findings classification:**
- Major Issue 1 (Global Search Anti-Pattern): A — global search initialized from mf1 inheriting cooled IF2 state, not from raw pomp object
- Major Issue 2 (Profile Likelihood base object): B — profile curves unreliable due to inherited cooled IF2 state (matches Human Issue #2)
- Major Issue 3 (Invalid SARIMA-vs-POMP comparison): B — SARIMA fitted to different time interval (~400 obs pre-pandemic) than SIRS (~313 obs), likelihoods not comparable (matches Human Issue #4)
- Major Issue 4 (Insufficient Computational Effort): B — sparse and scattered profile CI point clouds; reported log-likelihoods unreliable; profile CI calculations invalid (matches Human Issue #2)
- Major Issue 5 (No Benchmark Comparison): B — no valid benchmark since models fit different datasets and different observation models (matches Human Issue #4)
- Major Issue 6 (rho fixed implausibly): A — reporting rate fixed at 4e-5 without proper justification; should be estimated or profiled
- Major Issue 7 (Accumulator Semantics): A — H accumulates recoveries (dN_IR) rather than new infections (dN_SI), semantically incorrect
- Minor (%do% vs %dopar%): C — local search runs sequentially despite parallel backend being registered
- Minor (SARIMA prediction metrics): C — no quantitative prediction error reported for SARIMA held-out interval
- Minor (sin/cos discrepancy): C — text defines seasonality with cos but code implements sin
- Minor (BoxCox hardcoded shift): D — hardcoded +1050 shift in Box-Cox transformation is unexplained (matches Human Issue #3)
- Minor (rho arithmetic): C — arithmetic underlying rho calculation not shown; weekly vs. annual case count confusion
- Minor (poor man's profile): C — scatter plots include earlier local-search results rather than filtering to global-search results only
- Minor (CI not reported): C — profile CI bounds computed but not explicitly reported in conclusion
- Minor (informal reference): C — Reference [0] citing office hours is unverifiable
- Minor (code quality): C — numerous commented-out code blocks make it unclear which version was run
- Minor (missing model diagnostics): C — no ESS monitoring results or conditional log-likelihood plots presented

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 4 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 1 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by findings: "profile likelihood failure renders central hypothesis untestable" and "IF2 non-convergence")
- Human Issue #3: covered (matched by finding: "likelihood comparison across model classes requires care — different scales due to Box-Cox and different time windows")
- Human Issue #4: covered (matched by finding: "likelihood comparison across model classes requires care — different scales due to Box-Cox and different time windows")

**Findings classification:**
- [22.20.1/2] Profile likelihood failure renders central hypothesis untestable: B — degenerate CIs and scattered profile points indicate optimization has not converged (matches Human Issue #2)
- [22.20.4] IF2 non-convergence: B — local search traces for key parameters continue to trend upward after 50 IF2 iterations (matches Human Issue #2)
- [22.20.5] Mathematical description uses cos, code uses sin: A — quarter-period inconsistency between written model and implementation
- [22.20.6] b-profile trace plot copy-paste error: A — code groups by round(a,5) and plots a instead of b, producing incorrect visualization
- [22.20.3] Likelihood comparison across model classes requires care: D — SARIMA log-likelihood on Box-Cox transformed data over 2010–2020 vs SIRS on raw counts over 2015–2021 are not comparable (matches Human Issues #3 and #4)
- [22.20.7] Reporting rate rho fixed without sensitivity analysis: C — rho derived from back-of-envelope calculation and fixed, propagating unquantified uncertainty into a and b
- [22.20.8] Best-fit mu_IR = 7/week implies ~1-day recovery: C — implausibly fast for influenza; units and prior constraints should be verified
- [22.20.M1] dmeasure likelihood guard lik=0 numerically incorrect: C — should return R_NegInf in log context rather than 0 to avoid distorting particle weights
- Np=1000 at run_level=3 is low: C — standard practice uses Np=5000 for final inference
- AIC table headers garbled: C — incomplete column headers and apparently rescaled values

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 2 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 1 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 7 | 6 | 3 | 2 |
| B (AI major, human also found) | 2 | 3 | 4 | 2 |
| C (AI minor, human missed) | 5 | 5 | 9 | 5 |
| D (AI minor, human also found) | 1 | 1 | 1 | 1 |
| E (Human found, AI missed) | 1 | 1 | 1 | 1 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 2 | 1 | 1 | 3/4 = 75% | 7 | 5 | 12/15 = 80% |
| Charlie | 3 | 1 | 1 | 3/4 = 75% | 6 | 5 | 11/15 = 73% |
| Doug | 4 | 1 | 1 | 3/4 = 75% | 3 | 9 | 12/17 = 71% |
| Evan | 2 | 1 | 1 | 3/4 = 75% | 2 | 5 | 7/10 = 70% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #1: For exploratory data analysis and/or ARMA and/or wavelets, it might be worth looking at the logarithm of the data since population dynamics are usually closer to linear on a log scale. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 1 out of 4 human issues (25%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

(none)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |
