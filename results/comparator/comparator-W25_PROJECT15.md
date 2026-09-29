# Comparator Analysis — W25 Project 15

---

## Human Issues

1. Why is GARCH selected by log-likelihood not AIC? And, are you sure the software is reporting the actual likelihood not some approximation? Quantities called log-likelihood for GARCH software are sometimes not exactly the log-likelihood. It would be worth saying how you know your numbers are correct.

2. Fig. 7 shows long tails, not "adequate except for slight heavy-tail deviations." Trying a t-distributed GARCH would lead to substantial improvement, as the project later finds for stochastic volatility.

3. Note that the GARCH log-likelihoods do not satisfy nesting. Mathematically, e.g., (p,q)=(3,2) includes (3,1) so should not have a lower maximized likelihood.

4. Interestingly, with the t-distribution, the likelihood does not decrease through iterations, at least for the better mode.

5. Various models are investigated, and it would be nice to have more direct comparison. At least, a table with all the likelihoods. Perhaps also some analysis of conditional log-likelihoods at each time point to see which observations the models differ on.

6. "Even though we cannot directly compare loglikelihood from tseries::garch [12], we can still argue that GARCH(3,1) is the most promising one" could be confusing. Is this calculated conditionally on some initial data? It needs explanation to say something is wrong but we use it anyway.

---

## Alex

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Log-likelihood comparison informal and misleading — tseries::garch uses a conditional likelihood that differs from the full likelihood, addressing the human's concern about whether the software reports the actual likelihood")
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "Log-likelihood comparison informal and misleading — authors acknowledge the tseries::garch incomparability at line 287 but do not adequately account for it, matching the human's concern about the confusing statement that something is wrong but used anyway")

**Findings classification:**
- Finding 1 (Duplicate stew file name invalidates New Global Search): A — duplicate stew cache key causes second global search to silently reuse first search results
- Finding 2 (Initial global search box excludes claimed superior mode): A — search box constrained to phi in [0.95,0.99] cannot discover phi ~0.5 identified as best
- Finding 3 (Heston SV code does not match stated model equation): A — code implements phi*sqrt(V) instead of phi*V, making the fitted model different from the described model
- Finding 4 (Potential FNG covariate length mismatch): A — fng_subset and merged_df may have different row counts, causing silent recycling or crash
- Finding 5 (No formal statistical inference for FG Index effect): A — no LRT, profile likelihood CI, or test of H0: gamma=0 to support the central claim
- Finding 6 (Log-likelihood comparison informal and potentially misleading): B — different response variables and tseries conditional vs particle-filter full likelihood make comparisons invalid (matches Human Issues #1 and #6)
- Finding 7 (sigma_nu converging to zero not discussed as boundary problem): A — parameter at boundary of support signals possible misspecification but is not diagnosed
- Finding 8 (Fixed df=5 for t-distribution not justified rigorously): C — experimenting with df values 3–25 without showing results or profiling is ad hoc
- Finding 9 (Contradictory claims about local vs global search sign of gamma): C — positive gamma in local search vs negative in global search signals identifiability problem not investigated
- Finding 10 (New Global Search narrative internally inconsistent): C — discussion of differences between searches is unfounded because both return the same cached results
- Finding 11 (Both simple SV global searches overwrite the same output file): C — btc_global_params.csv overwritten by t-distribution results, silently destroying normal-distribution output
- Finding 12 (Justification for differencing FG Index is incomplete): C — visual ACF inspection used instead of ADF/KPSS test; differencing shifts economic interpretation not discussed
- Finding 13 (Title typo — leading "V" missing): C — title reads "olatility analysis on Bitcoin returns"
- Finding 14 (Figure 25 mislabeled as Local Search): C — global search pairs plot labeled as local search, copy-paste error
- Finding 15 (Several typographical and grammatical issues): C — multiple spelling errors, HTML tag errors in references, acknowledged AI polishing did not fix them

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: covered (matched by finding: "GARCH vs POMP log-likelihood comparison acknowledged as invalid but used in conclusions")
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "No consolidated model comparison table")
- Human Issue #6: covered (matched by finding: "GARCH vs POMP log-likelihood comparison acknowledged as invalid but used in conclusions")

**Findings classification:**
- Finding 1 (Breto and SSV models fitted to different data): A — cross-family log-likelihood comparisons invalid due to different data series
- Finding 2 (stew() filename collision): A — "New Global Search" silently reloads first-search results
- Finding 3 (Heston code does not implement stated equation): A — phi*sqrt(V) in code vs phi*V in text
- Finding 4 (GARCH vs POMP comparison invalid but used): B — tseries::garch likelihood not on same scale; used in conclusions despite acknowledged invalidity (matches Human Issues #1 and #6)
- Finding 5 (No profile likelihoods or confidence intervals): A — no profiles for any of the six models
- Finding 6 (sigma_nu converges to boundary): A — leverage parameter degeneracy not investigated as model misspecification
- Finding 7 (FG Index from live API): A — analysis not reproducible due to shifting API window
- Finding 8 (t df by trial-and-error): C — degrees of freedom fixed informally without reported likelihoods
- Finding 9 ("New Global Search" is local refinement): C — narrow parameter box around prior optimum, not a genuine global search
- Finding 10 (H_0 non-convergence not remediated): C — initial condition instability unaddressed
- Finding 11 (gamma sign interpretation fragile): C — sign flips between local and global optima, no profile to support conclusion
- Finding 12 (Title typo): C — missing initial "V" in document title
- Finding 13 (Np=2000 below course standard): C — run_level=3 uses Np=2000 instead of Np=5000
- Finding 14 (No consolidated model comparison table): D — six models compared without a summary table (matches Human Issue #5)
- Finding 15 (dFNG zero-padding without justification): C — ad hoc initialization of differenced FNG covariate at t=0

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "cross-model log-likelihood comparisons are invalid due to different datasets/measurement distributions")
- Human Issue #6: covered (matched by finding: "no benchmark comparison against non-mechanistic models; GARCH log-likelihood acknowledged as incomparable but conclusions still drawn from it")

**Findings classification:**
- Finding 1 (IF2 global search initialized from previous mif2 result): A — global search for all POMP models anchored to local optimum by passing prior mif2 result instead of base pomp object
- Finding 2 (initial particle filter on simulated data): A — initial log-likelihood benchmarks computed on simulated rather than real data, making them meaningless as real-data benchmarks
- Finding 3 (Heston process equation mismatch): A — implemented Csnippet uses phi*sqrt(V) instead of phi*V, producing materially different dynamics from the stated model
- Finding 4 (no profile likelihoods): A — no profile likelihoods computed for any model; parameter identifiability not formally assessed despite noted convergence anomalies
- Finding 5 (no benchmark comparison; invalid GARCH comparison): B — GARCH log-likelihood acknowledged as not directly comparable to POMP log-likelihoods yet conclusions still assert POMP outperforms GARCH without quantitative basis (matches Human Issue #6)
- Finding 6 (duplicate stew() filename): A — second global search for basic Breto uses same filename as first search, so stew() loads prior results rather than running new search
- Finding 7 (cross-model log-likelihood comparisons invalid): B — models use different data objects and measurement distributions, making log-likelihood comparisons across the six model families numerically invalid (matches Human Issue #5)
- Finding 8 (degrees of freedom fixed without justification): C — Student's t df=5 chosen by informal visual inspection rather than likelihood maximization or quantitative model selection
- Finding 9 (FG Index fetched live from API): C — Fear & Greed Index fetched at render time from live API, violating reproducibility; results will differ on different render dates
- Finding 10 (stationarity assessed only by ACF): C — FG Index stationarity concluded from ACF inspection alone with no formal unit-root test (ADF, KPSS, or Phillips-Perron)
- Finding 11 (sigma_nu converges to zero): C — sigma_nu convergence to zero implies degenerate leverage process; text notes it but does not investigate via profile likelihood
- Finding 12 (title typo): C — YAML title reads "olatility" missing initial 'V'
- Finding 13 (H_0 non-convergence dismissed): C — H_0 non-convergence noted but dismissed without investigation; affects reliability of all co-moving parameter estimates
- Finding 14 (no final MLE parameter table): C — final MLE parameter vectors only appear inline in print() calls; no consolidated table for all six models
- Finding 15 (model comparison narrative inconsistent): C — text treats initial particle filter log-likelihoods at test parameters as evidence of fitted model performance rather than global-search MLE values

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: covered (matched by finding: "25.15.4 — GARCH benchmark comparison needs clarification; tseries::garch likelihoods may reflect normalization conventions rather than actual log-likelihoods")
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "25.15.M3 — Missing consolidated model comparison table with all likelihoods")
- Human Issue #6: covered (matched by finding: "25.15.4 — GARCH benchmark comparison needs clarification; tseries::garch likelihoods cannot be directly compared yet are used as a beaten benchmark")

**Findings classification:**
- 25.15.1: A — SSV process equation inconsistency between code and stated model (phi*sqrt(V) vs phi*V)
- 25.15.2: A — No profile likelihoods or confidence intervals reported for any model
- 25.15.3: A — Gamma_fng sign instability between local and global search; sign of key parameter unidentified
- 25.15.4: B — GARCH benchmark comparison needs clarification; tseries::garch likelihood normalization issues make the comparison invalid (matches Human Issues #1 and #6)
- 25.15.5: A — Gamma interpretation conflates changes in FNG index with levels
- 25.15.M1: C — ACF used without formal test (ADF/KPSS) to justify differencing of FG index
- 25.15.M2: C — Degrees of freedom for t-distribution selected informally without likelihood justification
- 25.15.M3: D — Missing consolidated model comparison table with all likelihoods and parameter counts (matches Human Issue #5)
- 25.15.M4: C — Inconsistent reported likelihood for SSV normal model (3899.52 vs 3957.105)
- 25.15.M5: C — sigma_nu converges near zero in modified Breto models suggesting weak leverage identification
- 25.15.M6: C — No reproducibility archive or standalone script linked
- 25.15.M7: C — Typos and text errors throughout

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 6 | 6 | 5 | 4 |
| B (AI major, human also found) | 1 | 1 | 2 | 1 |
| C (AI minor, human missed) | 8 | 7 | 8 | 6 |
| D (AI minor, human also found) | 0 | 1 | 0 | 1 |
| E (Human found, AI missed) | 4 | 3 | 4 | 3 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 1 | 0 | 4 | 2/6 = 33% | 6 | 8 | 14/15 = 93% |
| Charlie | 1 | 1 | 3 | 3/6 = 50% | 6 | 7 | 13/15 = 87% |
| Doug | 2 | 0 | 4 | 2/6 = 33% | 5 | 8 | 13/15 = 87% |
| Evan | 1 | 1 | 3 | 3/6 = 50% | 4 | 6 | 10/12 = 83% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #2: Fig. 7 shows long tails, not "adequate except for slight heavy-tail deviations." Trying a t-distributed GARCH would lead to substantial improvement, as the project later finds for stochastic volatility. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #3: Note that the GARCH log-likelihoods do not satisfy nesting. Mathematically, e.g., (p,q)=(3,2) includes (3,1) so should not have a lower maximized likelihood. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #4: Interestingly, with the t-distribution, the likelihood does not decrease through iterations, at least for the better mode. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 3 out of 6 human issues (50%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

(none)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |
