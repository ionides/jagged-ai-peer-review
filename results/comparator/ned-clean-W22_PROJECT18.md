# Ned-Clean Analysis — W22 Project 18

## Human Issues

1. Annual data for only 40 years is somewhat limited; higher-frequency or longer historical data would be better.
2. The rationale for using ARMA(0,1) rather than ARMA(0,0) is weak — essentially no likelihood improvement for the extra parameter.
3. Too little data to fit a complex model like stochastic volatility with leverage; should start simpler or test whether leverage is needed.
4. Figure captions and numbers are missing.
5. Numbers should not be hard-coded in the Rmd document; they should be referenced using inline R code.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "ARMA(0,0) dismissed without adequate discussion")
- Human Issue #3: covered (matched by finding: "annual data inappropriate for GARCH/volatility model")
- Human Issue #4: missed
- Human Issue #5: missed

**Findings classification:**
- #1 (Corrupted Profile Likelihood CSV): A — column-ordering bug in oilprice_params.csv invalidates profile likelihood
- #2 (Profile Likelihood Interpretation Incorrect): A — authors misread their own profile plot, compounded by CSV bug
- #3 (Annual Data Inappropriate for GARCH/Volatility): B — applying SV model to 40 annual observations is methodologically inappropriate (matches Human Issue #3)
- #4 (GARCH AIC Table Is an Image): A — garch.jpg breaks reproducibility; kable line is commented out
- #5 (POMP Model Copied from Prior Year): A — code and structure copied from W21 Shanghai project without adaptation
- #6 (Filtering on Simulated Data Uninformative): A — log-likelihood of -65.07 on simulated data is presented but never interpreted
- #7 (Local Search Uses Single Starting Point): A — 20 replicates all from same start does not constitute local search
- #8 (Global Search Box Derived from Local Search Pairs): A — circular derivation of global box from local search results
- #9 (phi Hits Upper Boundary): C — optimizer is artificially constrained; phi concentrates at 0.99 boundary
- #10 (ARMA(0,0) Dismissed Without Adequate Discussion): D — rationale for choosing ARMA(0,1) over AIC-optimal ARMA(0,0) is not rigorous (matches Human Issue #2)
- #11 (GARCH Log-Likelihood Comparison Incorrect): C — GARCH logLik from fGarch may be per-observation; cross-model AIC comparison not made consistently
- #12 (Convergence Diagnostics Not Adequately Discussed): C — non-convergence noted but no corrective action taken
- #13 (No Simulation-Based Model Checking): C — no simulated trajectories compared to observed data after fitting
- #14 (Data Subsetting Row Indexing Fragile): C — hard-coded oil[120:160,] not verified against intended years
- #15 (Research Question Overly Broad): C — "Can we use time series analysis?" is trivially answered

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "ARMA model selection bypasses AIC-optimal model without adequate justification")
- Human Issue #3: covered (matched by finding: "small sample size not discussed as limitation for POMP model")
- Human Issue #4: missed
- Human Issue #5: missed

**Findings classification:**
- #1 (Profile likelihood non-functional — phi never varied): A — all 100 profile runs return phi = 0.9928931; profile is degenerate
- #2 (Profile plot mixes two incomparable groups): A — rows 1-120 and 121-220 in CSV are on different scales, producing a misleading figure
- #3 (POMP AIC claim is inverted): A — POMP has highest AIC (16.45); ARMA(0,0) has lowest (10.87)
- #4 (GARCH AIC table uses different package than reported log-likelihood): A — tseries::garch vs. fGarch::garchFit; normalizations differ
- #5 (No simulation-based model diagnostics): A — no simulated trajectories vs. observed data; no ESS trace; no conditional log-likelihoods
- #6 (Section 5.4 pairs plot displays local search results, not global): A — r.if1 used instead of r.box in the pairs call
- #7 (COVID-era return included despite stated exclusion): C — oil[120:160,] captures 2019-2020 return, contradicting stated exclusion
- #8 (Text description of global search box does not match code): C — sigma_nu upper bound stated as 0.020 in text but coded as 0.015
- #9 (GARCH AIC table replaced by static image): C — kable() commented out; garch.jpg cannot be verified against current code
- #10 (Nreps_local at run_level=3 is 20, not 40): C — below course standard of 40 starts
- #11 (ARMA model selection bypasses AIC-optimal without adequate justification): D — ARMA(0,0) dismissed; circular reasoning about limited data (matches Human Issue #2)
- #12 (GARCH residuals heavy-tailed but no alternative error distribution): C — Student-t GARCH not considered despite heavy tails in QQ plot
- #13 (Filtering on simulated data not interpreted): C — logLik of -65.07 reported but purpose not explained
- #14 (No ARMA/statistical benchmark comparison for POMP): C — cross-model comparison uses inconsistent normalizations
- #15 (Small sample size not discussed as limitation for POMP model): D — 6 parameters fit to 40 observations; ratio not discussed; broken profile prevents identifiability check (matches Human Issue #3)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Extremely Small Sample Size (n=39) Undermines All Model Inferences")
- Human Issue #2: covered (matched by finding: "ARMA model selection reasoning is circular")
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed

**Findings classification:**
- #1 (Global Search Initialized from Previous mif2 Result): A — if1[[1]] passed to mif2() instead of base pomp object; cooling schedule already decayed
- #2 (Profile Likelihood Seeded from Pre-Global-Search CSV): A — profile block runs before global search writes to CSV; profile seeded from local-only results
- #3 (Profiled Parameter phi Not Fixed During Profile IF2): A — c() concatenation creates duplicate phi names; grid value may be silently overridden by params_test
- #4 (No Non-Mechanistic Benchmark Comparison): A — POMP vs. GARCH/ARMA comparison uses inconsistent log-likelihood scales; no unified table
- #5 (Extremely Small Sample Size): B — n=39 too small for 6-parameter SV; fix recommends monthly/quarterly data (matches Human Issue #1)
- #6 (Poor Convergence Not Addressed): A — phi and sigma_eta do not stabilize; no corrective action taken despite self-acknowledgment
- #7 (GARCH Log-Likelihood Scale Discrepancy): A — fGarch logLik may be per-observation vs. total; scale not clarified
- #8 (AIC Computation Reliability Questioned): A — maximum over replicates from non-converged search may be spurious
- #9 (Profile Likelihood Interpretation Reversal): A — points above threshold are inside CI, not outside; text reverses this; phi < 0 description impossible given logit transform
- #10 (No ESS/Conditional Log-Likelihood Diagnostics): A — no per-time-step ESS, no conditional log-likelihood plot, no forward simulation from filtering distribution
- Minor — Data subsetting by row number: C — oil[120:160,] should use year-based filtering
- Minor — GARCH AIC table is static image: C — kable() commented out; garch.jpg not verifiable
- Minor — ARMA model selection reasoning circular: D — ARMA(0,0) dismissed using higher AIC as evidence of dependence; misuses AIC (matches Human Issue #2)
- Minor — Filtering on simulated data not informative: C — logLik of -65.07 applies to simulated not real data
- Minor — nprof=2 too few restarts per grid cell: C — only 2 starts per profile grid value on volatile likelihood surface
- Minor — No sessionInfo or package versions: C — pomp API changes across versions; analysis may not reproduce
- Minor — References cite 2020 notes for 2022 project: C — should cite 531w22 course notes

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 9 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: covered (matched by finding: "N=40 annual observations too small for 6-parameter SV model")
- Human Issue #2: covered (matched by finding: "ARMA(0,0) finding dismissed without scientific discussion")
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed

**Findings classification:**
- 22.18.3 (POMP does not have lowest AIC): A — ARMA(0,0) AIC = 10.87; POMP AIC = 16.45; conclusion is inverted
- 22.18.2 (Profile likelihood over phi is degenerate): A — logLik ≈ 0.0 in profile is numerical failure, not genuine likelihood; CI threshold invalid
- 22.18.4 (Global search MLE sigma_nu = 3.59 is implausible): A — 180x the upper bound of local search range; uninvestigated numerical artifact
- 22.18.5 (No confidence intervals for any POMP parameter): A — profile is malformed; no MCAP or likelihood-ratio CIs reported
- 22.18.N1 (N=40 too small for 6-parameter SV model): B — non-convergence, degenerate profile, and implausible MLE all trace to insufficient data; suggests higher-frequency data (matches Human Issue #1)
- 22.18.6 (GARCH log-likelihood scale convention unclear): A — logLik = -3.33 may be per-observation; direct comparison to POMP total logLik is unverified
- 22.18.7 (Local IF2 convergence not achieved): C — diverging logLik traces and non-converged mu_h at iteration 200; Nmif not increased
- 22.18.M1 (ARMA(0,0) dismissed without scientific discussion): D — white noise result has economic interpretation; dismissal is unscientific (matches Human Issue #2)
- 22.18.N2 (Section 5.1 references SSE Composite Index): C — copy-paste artifact from referenced W21 project; crude oil analysis mislabeled
- 22.18.M2 (Gaussian measurement noise not acknowledged as limitation): C — Student-t extension exists and is more realistic for financial returns
- 22.18.9 (Np, Nmif, replicates not reported in manuscript): C — computational adequacy cannot be assessed by reader

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 7 | 6 | 9 | 5 |
| B (AI major, human also found) | 1 | 0 | 1 | 1 |
| C (AI minor, human missed) | 6 | 7 | 6 | 4 |
| D (AI minor, human also found) | 1 | 2 | 1 | 1 |
| E (Human found, AI missed) | 3 | 3 | 3 | 3 |

---

## Per-Reviewer Metrics

| Reviewer | B | D | E | Human Recall | A | C | AI-Unique Rate |
|----------|--:|--:|--:|-------------:|--:|--:|---------------:|
| Alex | 1 | 1 | 3 | 2/5 = 40% | 7 | 6 | 13/15 = 87% |
| Charlie | 0 | 2 | 3 | 2/5 = 40% | 6 | 7 | 13/15 = 87% |
| Doug | 1 | 1 | 3 | 2/5 = 40% | 9 | 6 | 15/17 = 88% |
| Evan | 1 | 1 | 3 | 2/5 = 40% | 5 | 4 | 9/11 = 82% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #3: Too little data to fit a complex model like stochastic volatility with leverage; should start simpler or test whether leverage is needed.
- Human Issue #4: Figure captions and numbers are missing.
- Human Issue #5: Numbers should not be hard-coded in the Rmd document; they should be referenced using inline R code.

Count: 3 out of 5 human issues (60%) were missed by every reviewer.

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #1 (annual data limited; higher-frequency preferred): covered by Doug and Evan, missed by Alex and Charlie — not a unique find for any single reviewer.
- Human Issue #2 (ARMA(0,1) rationale weak): covered by all four reviewers — not a unique find.

No human issue was covered by exactly one reviewer and missed by all others.

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |

### Universal AI-only flags

Issues raised as Major by every reviewer that the human did not mention:

- All four reviewers flagged that the POMP AIC conclusion is inverted (POMP has the highest AIC, not the lowest; ARMA(0,0) at 10.87 beats POMP at 16.45). The human did not raise this.
- All four reviewers flagged that the profile likelihood is degenerate or invalid (corrupted CSV / phi never varied / degenerate evaluations). The human did not raise this.
- Three of four reviewers (Charlie, Doug, Evan) flagged the GARCH log-likelihood scale discrepancy / cross-package normalization issue. Alex also flagged this as MODERATE. The human did not raise this.
- Three of four reviewers (Alex, Charlie, Doug) flagged no simulation-based model diagnostics after fitting. Evan did not flag this as a separate finding. The human did not raise this.

Universal AI-only Major flags (all four reviewers): 2 (inverted AIC conclusion; degenerate profile likelihood).
