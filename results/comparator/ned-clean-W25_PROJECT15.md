# Ned-Clean Analysis — W25 Project 15

---

## Human Issues

1. GARCH model selection uses log-likelihood rather than AIC, and it is unclear whether the software reports the true likelihood or an approximation; the authors do not explain how they verified the numbers are correct.
2. Fig. 7 shows long tails that are not "adequate except for slight heavy-tail deviations"; a t-distributed GARCH would substantially improve fit.
3. The GARCH log-likelihoods do not satisfy nesting (e.g., GARCH(3,2) should have a log-likelihood at least as high as GARCH(3,1) because it nests it).
4. Various models are investigated but a direct comparison is missing; at minimum, a table with all likelihoods is needed, and possibly conditional log-likelihood analysis by time point.
5. The statement "Even though we cannot directly compare loglikelihood from tseries::garch, we can still argue that GARCH(3,1) is the most promising one" is confusing and needs explanation — it says something is wrong but proceeds to use it anyway.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "Log-likelihood comparison across models informal and misleading; authors acknowledge tseries::garch non-comparability at line 287 but do not adequately account for it")

**Findings classification:**
- Finding #1 [MAJOR] Duplicate stew() filename invalidates new global search: A — stew cache collision silently reuses first search results
- Finding #2 [MAJOR] Initial global search box excludes claimed superior mode: A — search box disjoint from the mode identified as superior
- Finding #3 [MAJOR] Heston SV code does not match stated model equation: A — phi*sqrt(V) in code vs. phi*V in stated model
- Finding #4 [MAJOR] Potential FNG covariate length mismatch: A — independent API subset may differ in row count from merged dataset
- Finding #5 [MAJOR] No formal statistical inference for FG Index effect: A — no LRT, profile likelihood, or CI for gamma; conclusion unsupported
- Finding #6 [MAJOR] Log-likelihood comparison informal and potentially misleading: B — different response variables; tseries::garch conditional likelihood vs. POMP full likelihood (matches Human Issue #5)
- Finding #7 [MAJOR] sigma_nu converging to zero not discussed as boundary problem: A — potential model misspecification or degenerate solution not explored
- Finding #8 [MODERATE] Fixed df=5 for t-distribution not rigorously justified: C — no log-likelihoods shown across tested df values
- Finding #9 [MODERATE] Contradictory gamma sign between local and global search: C — positive vs. negative gamma, no resolution
- Finding #10 [MODERATE] New global search narrative internally inconsistent: C — narrative written based on expected rather than actual outputs (consequence of stew collision)
- Finding #11 [MODERATE] Both simple SV global searches overwrite same output CSV: C — normal-distribution results silently destroyed
- Finding #12 [MODERATE] Justification for differencing FG Index incomplete: C — no ADF/KPSS test; interpretive shift not discussed
- Finding #13 [MINOR] Title contains a typo ("olatility"): C — missing leading "V"
- Finding #14 [MINOR] Figure 25 mislabeled as "Local Search": C — copy-paste error in global search pairs plot label
- Finding #15 [MINOR] Several typographical and grammatical issues: C — "Stuent's", "aerbecause", "Chapte-15", HTML tag errors in references

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
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "Model comparison table absent; log-likelihoods scattered and incomparable; formal AIC comparison needed")
- Human Issue #5: covered (matched by finding: "No non-mechanistic benchmark; tseries::garch cannot be directly compared to POMP log-likelihoods but Conclusions still asserts Breto outperforms")

**Findings classification:**
- Finding #1 [Major] stew() filename collision invalidates new global search: A — same filename causes cached first-search results to be reloaded
- Finding #2 [Major] Global search initialization from prior mif2 result: A — inherited cooling schedule means near-zero perturbations from random starts
- Finding #3 [Major] No profile likelihoods; parameter identifiability unresolved: A — multimodal structure acknowledged but not formally resolved
- Finding #4 [Major] No non-mechanistic benchmark for POMP models: B — tseries::garch acknowledged as incomparable yet used for benchmark conclusions (matches Human Issue #5)
- Finding #5 [Major] Heston process equation misspecified: A — phi*sqrt(V) vs. phi*V in code
- Finding #6 [Major] Initial particle filter on simulated data presented as benchmark: A — log-likelihood from simulated data not on same scale as real-data inference
- Finding #7 [Major] Model comparison table absent; log-likelihoods scattered and incomparable: B — no consolidated table; different Np, pfilter replicates, and data objects across models (matches Human Issue #4)
- Finding #8 [Minor] gamma_fng conclusion from single point estimate without uncertainty: C — no CI; local and global search sign discrepancy unresolved
- Finding #9 [Minor] H_0 non-convergence acknowledged but not addressed: C — non-convergence of initial condition parameter not diagnosed
- Finding #10 [Minor] FG Index stationarity justification informal: C — no ADF/KPSS test; slowly decaying ACF alone insufficient
- Finding #11 [Minor] rw.sd values uniform across parameters with no rationale: C — uniform 0.02/0.1 may impede convergence given sigma_nu near zero
- Finding #12 [Minor] t-distribution df chosen by informal experimentation: C — no likelihood criterion or profile over df values
- Finding #13 [Minor] stew() not used for modified Breto and Heston searches: C — reproducibility reduced
- Finding #14 [Minor] Title typo and code quality issues: C — missing "V"; redundant library calls; plan(multisession) mismatch
- Finding #15 [Minor] References incomplete and improperly formatted: C — unclosed HTML tags; missing author/title on reference; duplicated footnote IDs

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "No benchmark comparison; Conclusions asserts Breto outperforms GARCH despite flagging non-comparability of tseries::garch log-likelihoods")

**Findings classification:**
- Finding #1 [Major] Global search IF2 initialized from previous mif2 result: A — inherited cooling leaves effectively no exploration from random starts
- Finding #2 [Major] Initial particle filter benchmark computed on simulated data: A — log-likelihood from simulated data not comparable to real-data inference
- Finding #3 [Major] Heston process equation in code does not match text specification: A — phi*sqrt(V) instead of phi*V; materially different dynamics
- Finding #4 [Major] No profile likelihoods computed; identifiability not formally assessed: A — sigma_nu and H_0 non-convergence signals unresolved
- Finding #5 [Major] No benchmark comparison against non-mechanistic models: B — GARCH non-comparability flagged but Conclusions still claims Breto outperforms (matches Human Issue #5)
- Finding #6 [Major] Duplicate stew() filename invalidates new global search: A — narrowed-box search never executed; first-search results reloaded
- Finding #7 [Major] Cross-model log-likelihood comparisons invalid due to different datasets: A — different data objects and transformations across model families
- Finding #8 [Minor] Degrees of freedom for t-distribution fixed without formal justification: C — informal experimentation without likelihood criterion
- Finding #9 [Minor] Data reproducibility: FG Index fetched live from API: C — results will shift as API returns most recent 2000 days
- Finding #10 [Minor] Stationarity of FG Index assessed only by ACF inspection: C — no formal unit-root test (ADF, KPSS)
- Finding #11 [Minor] sigma_nu converges to zero without identifiability discussion: C — degenerate leverage process not investigated
- Finding #12 [Minor] Title typo: C — "olatility" missing leading "V"
- Finding #13 [Minor] H_0 non-convergence dismissed without investigation: C — non-convergence of initial log-volatility not diagnosed
- Finding #14 [Minor] No final MLE parameter table for reproducibility: C — estimates reported only inline via print() calls
- Finding #15 [Minor] Model comparison narrative inconsistent with POMP log-likelihood direction: C — initial pfilter log-likelihoods misrepresented as fitted model performance

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

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "Missing consolidated model comparison table with all models, parameter counts, max log-likelihoods, SEs, and AIC values")
- Human Issue #5: covered (matched by finding: "GARCH benchmark comparison needs clarification; paper cannot simultaneously flag non-comparability and use GARCH as a beaten benchmark")

**Findings classification:**
- Finding #1 [Major] SSV process equation inconsistency between code and model: A — phi*sqrt(V) in code vs. phi*V in stated model; different dynamical system
- Finding #2 [Major] No profile likelihoods or confidence intervals for any model: A — gamma_fng sign and significance unquantified
- Finding #3 [Major] Gamma_fng sign instability between local and global search: A — local (+0.13) vs. global (-0.89) at indistinguishable log-likelihoods; sign not identified
- Finding #4 [Major] GARCH benchmark comparison needs clarification: B — normalization conventions in tseries::garch; paper flags non-comparability then claims Breto outperforms (matches Human Issue #5)
- Finding #5 [Major] Gamma interpretation conflates changes with levels: A — differenced FG index governs effect of changes, not level; interpretation in text is incorrect
- Finding M1 [Minor] ACF used without formal test to justify differencing: C — no ADF/KPSS; slowly decaying ACF consistent with stationary long-memory
- Finding M2 [Minor] Degrees of freedom for t-distribution selected informally: C — no log-likelihoods reported across df values; implicit model selection without correction
- Finding M3 [Minor] Missing consolidated model comparison table: D — six models' best log-likelihoods and MC SEs scattered across sections (matches Human Issue #4)
- Finding M4 [Minor] Inconsistent reported likelihood for SSV normal model: C — text says ~3899.52 but code output reports 3957.105
- Finding M5 [Minor] sigma_nu converges near zero in modified Breto models: C — G random walk nearly degenerate; leverage weakly identified
- Finding M6 [Minor] No reproducibility archive: C — no standalone script file or data archive linked
- Finding M7 [Minor] Typos and text errors: C — "aerbecause", "divergenece", "demanded return", "mispecified"

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
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 6 | 5 | 6 | 4 |
| B (AI major, human also found) | 1 | 2 | 1 | 1 |
| C (AI minor, human missed) | 8 | 8 | 8 | 6 |
| D (AI minor, human also found) | 0 | 0 | 0 | 1 |
| E (Human found, AI missed) | 4 | 3 | 4 | 3 |

---

## Per-Reviewer Metrics

Human Recall = (B+D) / (B+D+E)
AI-Unique Rate = (A+C) / (A+B+C+D)

| Reviewer | B | D | E | Human Recall | A | C | AI-Unique Rate |
|----------|--:|--:|--:|-------------:|--:|--:|---------------:|
| Alex | 1 | 0 | 4 | 1/5 = 20.0% | 6 | 8 | 14/15 = 93.3% |
| Charlie | 2 | 0 | 3 | 2/5 = 40.0% | 5 | 8 | 13/15 = 86.7% |
| Doug | 1 | 0 | 4 | 1/5 = 20.0% | 6 | 8 | 14/15 = 93.3% |
| Evan | 1 | 1 | 3 | 2/5 = 40.0% | 4 | 6 | 10/12 = 83.3% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #1: GARCH model selection by log-likelihood not AIC; whether software reports true likelihood or approximation — missed by all 4 reviewers.
- Human Issue #2: Fig. 7 shows long tails not adequately described; t-distributed GARCH would substantially improve fit — missed by all 4 reviewers.
- Human Issue #3: GARCH log-likelihoods do not satisfy nesting — missed by all 4 reviewers.

Count: 3 out of 5 human issues were consensus misses (60%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer (all others missed):

- Human Issue #4 (missing comparison table): covered by Charlie and Evan; not unique to one reviewer.
- Human Issue #5 (confusing tseries::garch statement): covered by Alex, Charlie, Doug, and Evan; not unique.

No human issue was covered by exactly one reviewer and missed by all others.

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |

### Universal AI-only flags

Issues raised as Major by every reviewer that the human did not mention:

- Heston/SSV process equation mismatch: phi*sqrt(V) in code vs. phi*V in stated model — raised as Major by Alex (#3), Charlie (#5), Doug (#3), and Evan (#1). Not mentioned by human.
- No profile likelihoods / parameter identifiability not formally assessed — raised as Major by Charlie (#3), Doug (#4), and Evan (#2); raised as Major by Alex (#5, framed as no formal inference for gamma). Effectively universal.
- stew() filename collision invalidating new global search — raised as Major by Alex (#1), Charlie (#1), and Doug (#6); not raised as Major by Evan (Evan raised it implicitly within discussion but did not list it as a separate finding). Raised by 3 of 4.
- Global search IF2 initialized from prior mif2 result — raised as Major by Charlie (#2) and Doug (#1); raised as part of Alex's broader concerns implicitly; not found by Evan. Raised by 2 of 4 explicitly.

Universal (all 4 reviewers as Major): Heston process equation mismatch. Count: 1.
Near-universal (3 of 4 as Major): stew() filename collision, no profile likelihoods. Count: 2.
