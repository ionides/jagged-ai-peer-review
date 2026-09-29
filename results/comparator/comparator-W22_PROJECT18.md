# Comparator Analysis — W22 Project 18

---

## Human Issues

1. Annual data for only 40 years is somewhat limited for fitting models. Would it be possible to get higher-frequency data? Or, once log-transformed, it might be meaningful to fit a longer time series to get a longer historical perspective.

2. The rationale for using ARMA(0,1) rather than ARMA(0,0) is weak. It seems like there is essentially no likelihood improvement for adding the one extra parameter. Likely, the estimated MA(1) coefficient is very close to zero.

3. This is too little data to fit a fairly complex model like stochastic volatility with leverage. Maybe start with a simpler POMP model, or test whether a model with no leverage is sufficient.

4. Figure captions and numbers would be appreciated by referees.

5. Where possible, numbers should not be hard-coded in the Rmd document. Rather, they should be referenced using inline R expressions.

---

## Alex

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Annual Data Is Inappropriate for a GARCH/Volatility Model — annual frequency and 39 observations make GARCH/SV modeling methodologically unsuitable")
- Human Issue #2: covered (matched by finding: "ARMA(0,0) Is Dismissed Without Adequate Discussion — decision to use ARMA(0,1) over AIC-preferred ARMA(0,0) is not rigorously justified")
- Human Issue #3: covered (matched by finding: "Annual Data Is Inappropriate for a GARCH/Volatility Model — annual frequency and 39 observations make GARCH/SV modeling methodologically unsuitable")
- Human Issue #4: missed
- Human Issue #5: missed

**Findings classification:**
- Finding 1 (Corrupted Profile Likelihood CSV): A — column ordering in oilprice_params.csv breaks at row 122, invalidating profile likelihood figure
- Finding 2 (Profile Likelihood Interpretation Incorrect): A — text misreads its own plot, claiming phi < 0 region is above CI threshold
- Finding 3 (Annual Data Inappropriate for GARCH/Volatility Model): B — 40 annual observations are methodologically unsuitable for GARCH and SV models designed for high-frequency data (matches Human Issues #1 and #3)
- Finding 4 (GARCH AIC Table Is an Image): A — table embedded as static image with actual code commented out, breaking reproducibility
- Finding 5 (POMP Model Copied from Prior Year): A — code essentially a direct copy of lecture-notes template with no model adaptation or leverage-term evaluation
- Finding 6 (Filtering on Simulated Data Uninformative): A — log-likelihood on simulated data reported without interpretation or comparison to expected value
- Finding 7 (Local Search Uses Only Single Starting Point): A — all 20 MIF2 replicates launched from identical starting parameter vector
- Finding 8 (Global Search Box Derived Circularly from Local Search): A — global search ranges read off local search pairs plot rather than set from independent reasoning
- Finding 9 (phi Hits Upper Boundary of Global Search Box): C — optimizer constrained at phi = 0.99 upper edge with no investigation of unit-root implication
- Finding 10 (ARMA(0,0) Dismissed Without Adequate Discussion): D — white-noise result rejected on weak grounds; ARMA(0,1) pursued because it had second-lowest AIC (matches Human Issue #2)
- Finding 11 (GARCH Log-Likelihood Comparison Incorrect): C — per-observation GARCH log-likelihood compared against POMP particle-filter log-likelihood without proper scaling
- Finding 12 (Convergence Diagnostics Not Adequately Discussed): C — non-convergence noted but no corrective action taken (increased Nmif, Np, or remediation)
- Finding 13 (No Simulation-Based Model Checking): C — fitted POMP model never used to simulate trajectories for comparison against observed data
- Finding 14 (Data Subsetting Row Indexing Fragile): C — hard-coded row indices oil[120:160,] undocumented and inconsistent with stated 40-year window
- Finding 15 (Research Question Overly Broad): C — stated question "can we use time series analysis?" is trivially answered; conclusion does not address it substantively

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Small sample size (40 observations) is not discussed as a limitation for the POMP model")
- Human Issue #2: covered (matched by finding: "ARMA model selection bypasses the AIC-optimal model without adequate justification")
- Human Issue #3: covered (matched by finding: "Small sample size (40 observations) is not discussed as a limitation for the POMP model")
- Human Issue #4: missed
- Human Issue #5: missed

**Findings classification:**
- Finding 1 (Profile likelihood non-functional — phi is never varied): A — profile runs all return the same phi value, defeating profiling
- Finding 2 (Profile plot mixes two incomparable groups): A — corrupted profile plot makes CI entirely invalid
- Finding 3 (POMP AIC claim is inverted — POMP has highest AIC): A — primary comparative conclusion is backwards
- Finding 4 (GARCH AIC table uses different package than reported log-likelihood): A — cross-model AIC comparisons use inconsistent normalizations
- Finding 5 (No simulation-based model diagnostics): A — no simulated trajectories compared to real data, no ESS trace
- Finding 6 (Section 5.4 pairs plot displays local search results, not global): A — diagnostic figure contradicts section narrative
- Finding 7 (COVID-era return included despite stated exclusion): C — data selection mismatch between text and code
- Finding 8 (Text description of global search box does not match code): C — sigma_nu upper bound differs between text and code
- Finding 9 (GARCH AIC table replaced by static image): C — live-rendered table commented out, reproducibility broken
- Finding 10 (Nreps_local=20, not course standard of 40): C — reduced local search starts at run_level=3
- Finding 11 (ARMA model selection bypasses AIC-optimal model): D — unjustified preference for ARMA(0,1) over ARMA(0,0) (matches Human Issue #2)
- Finding 12 (GARCH residuals heavy-tailed, no Student-t alternative considered): C — standard response to heavy tails not applied
- Finding 13 (Filtering on simulated data not interpreted): C — Section 5.2 sanity check is uninterpreted
- Finding 14 (No consistent benchmark comparison for POMP): C — cross-model comparison uses inconsistent normalizations
- Finding 15 (Small sample size not discussed as limitation for POMP): D — 40 observations insufficient for 6-parameter model not discussed (matches Human Issues #1 and #3)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Extremely Small Sample Size (n=39) Undermines All Model Inferences — recommends monthly/quarterly data")
- Human Issue #2: covered (matched by finding: "ARMA model selection reasoning is circular")
- Human Issue #3: covered (matched by finding: "Extremely Small Sample Size (n=39) Undermines All Model Inferences — notes overparameterized for this dataset")
- Human Issue #4: missed
- Human Issue #5: missed

**Findings classification:**
- Major-1 (Global Search Initialized from Previous mif2 Result): A — global box search passes `if1[[1]]` instead of base pomp object, invalidating global optimization claim
- Major-2 (Profile Likelihood Seeded from Pre-Global-Search CSV State): A — profile reads CSV before global search results are written, so profile is seeded from sub-global optimum
- Major-3 (Profiled Parameter φ Not Fixed During Profile IF2 Search): A — duplicate parameter names in `c(unlist(guesses[i,]), params_test)` may cause profile grid value to be silently overridden
- Major-4 (No Non-Mechanistic Benchmark Comparison): A — POMP AIC compared only to GARCH and ARMA without white-noise baseline on a common likelihood scale
- Major-5 (Extremely Small Sample Size, n=39): B — 39 annual observations too few for stochastic-volatility model with six parameters; recommends higher-frequency data or acknowledges overparameterization (matches Human Issues #1 and #3)
- Major-6 (Poor Convergence Self-Acknowledged but Not Addressed): A — authors acknowledge non-convergence of φ and σ_η but take no corrective action before reporting final estimates
- Major-7 (GARCH Log-Likelihood Scale Discrepancy): A — reported GARCH log-likelihood of -3.331 is not clarified as total vs. per-observation, making POMP comparison uninterpretable
- Major-8 (AIC Computation Uses Best Replicate Log-Likelihood): A — AIC from non-converged local search may reflect spurious particle-filter excursion rather than stable MLE
- Major-9 (Profile Likelihood Interpretation Reversal): A — authors misread profile plot, stating points above threshold are outside CI when they are inside it
- Major-10 (No Model Diagnostics: ESS and Conditional Log-Likelihoods): A — no ESS monitoring, per-step conditional log-likelihoods, or forward simulation presented
- Minor-1 (Data subsetting by row number): C — `oil[120:160,]` relies on dataset having exactly 160 rows; should filter by year programmatically
- Minor-2 (AIC table for GARCH uses static image): C — GARCH AIC table is a JPEG; code that computes it is commented out, harming reproducibility
- Minor-3 (ARMA model selection reasoning is circular): D — authors select ARMA(0,1) despite ARMA(0,0) having lower AIC, using higher AIC as evidence of dependence, which misuses AIC (matches Human Issue #2)
- Minor-4 (Filtering simulation on simulated data): C — particle filter run on simulated data rather than observed data; resulting log-likelihood does not characterize fit to real data
- Minor-5 (nprof=2 in profile): C — only 2 restarts per profile-grid cell across 50 grid values is very low for an unstable log-likelihood surface
- Minor-6 (No sessionInfo or package versions): C — pomp, fGarch, tseries, and forecast versions unspecified; analysis may not reproduce
- Minor-7 (References cite 2020 lecture notes): C — references 8 and 9 cite 2020 course notes for a 2022 project; 2022 notes should be cited

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 9 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: covered (matched by finding: "22.18.N1 — N=40 annual observations too small for 6-parameter SV model; suggests higher-frequency data")
- Human Issue #2: covered (matched by finding: "22.18.M1 — ARMA(0,0) dismissed without scientific discussion; paper selects ARMA(0,1) without justification")
- Human Issue #3: covered (matched by finding: "22.18.N1 — N=40 annual observations too small for 6-parameter SV model; suggests fixing parameters to reduce model complexity")
- Human Issue #4: missed
- Human Issue #5: missed

**Findings classification:**
- 22.18.3: A — POMP does not have the lowest AIC; stated conclusion is factually incorrect (ARMA(0,0) AIC=10.87 beats POMP AIC=16.45)
- 22.18.2: A — Profile likelihood over phi is degenerate and cannot support CI claims
- 22.18.4: A — Global search best estimate sigma_nu=3.59 is implausible and uninvestigated
- 22.18.5: A — No confidence intervals reported for any POMP parameter
- 22.18.N1: B — N=40 annual observations too small for 6-parameter SV model; underlies most technical failures (matches Human Issues #1 and #3)
- 22.18.6: A — Log-likelihood scale convention for GARCH unclear, making cross-model comparison unreliable
- 22.18.7: C — Local IF2 search does not achieve convergence for all parameters
- 22.18.M1: D — ARMA(0,0) finding dismissed without scientific discussion; paper selects ARMA(0,1) without justification (matches Human Issue #2)
- 22.18.N2: C — Section 5.1 header references SSE Composite Index rather than crude oil (copy-paste artifact)
- 22.18.M2: C — Gaussian measurement noise assumption not acknowledged as limitation for financial data
- 22.18.9: C — Np, Nmif, and number of IF2 replicates not reported in the manuscript

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 7 | 6 | 9 | 5 |
| B (AI major, human also found) | 1 | 0 | 1 | 1 |
| C (AI minor, human missed) | 6 | 7 | 6 | 4 |
| D (AI minor, human also found) | 1 | 2 | 1 | 1 |
| E (Human found, AI missed) | 2 | 2 | 2 | 2 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 1 | 1 | 2 | 3/5 = 60% | 7 | 6 | 13/15 = 87% |
| Charlie | 0 | 2 | 2 | 3/5 = 60% | 6 | 7 | 13/15 = 87% |
| Doug | 1 | 1 | 2 | 3/5 = 60% | 9 | 6 | 15/17 = 88% |
| Evan | 1 | 1 | 2 | 3/5 = 60% | 5 | 4 | 9/11 = 82% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #4: Figure captions and numbers would be appreciated by referees. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #5: Where possible, numbers should not be hard-coded in the Rmd document. Rather, they should be referenced using inline R expressions. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 2 out of 5 human issues (40%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

(none)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |
