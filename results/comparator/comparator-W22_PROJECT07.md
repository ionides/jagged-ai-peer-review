# Comparator Analysis — W22 Project 07

---

## Human Issues

1. Model is missing a normal error in the term $Y_n = \exp\{H_n/2\} \epsilon_n$.

2. Based on the GARCH analysis, one might try $\epsilon_n$ having a $t$ distribution rather than normal. The effective sample size plot also suggests that - there are some jumps that are large outliers under a normal model.

3. A simpler stochastic volatility model might be worth trying before advancing to stochastic volatility with leverage. See Section 4 of https://ionides.github.io/531w22/final_project/project14/Blinded.html for an example.

4. Conclusion: "improvements of log likelihood were not significant" moving from normal to t GARCH seems wrong - make a likelihood ratio test.

5. Conclusion: "The POMP models perform much better than the GARCH for both Ford and Tesla" does not seem to be supported by the likelihoods. But, it looks like the Tesla POMP model was fitted to a reduced length time series (for practical reasons of finishing the analysis) which is not described in the report.

6. An AIC table for ARMA(p,q) is mentioned but not shown.

7. "Other models with competitive AIC values are not invertible or causal, with polynomial roots inside of the unit circle" seems implausible, since `arima()` will never fit roots inside the unit circle, though they may be on the boundary or close to it.

8. Plotting simulations from the mechanistic models would allow us to visually assess the fitted models and compare the performance of the local to the global search.

9. Typo: "(why we want to use log return instead of return?)" should be deleted. Also, in technical contexts, we usually say "return" to refer to the so-called log return.

---

## Alex

**Coverage record:**
- Human Issue #1: covered (matched by finding: "POMP Model Description and State Variable Definition Are Inconsistent — text omits epsilon_n error term")
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "Tesla POMP Uses Only 365 Observations While Ford Uses All 1,258"; also matched by finding: "POMP vs. GARCH Comparison Is Invalid — Log-Likelihoods Are Not Comparable")
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: covered (matched by finding: "Incomplete Sentence Left in Introduction")

**Findings classification:**
- Finding 1 (Tesla POMP 365 obs vs Ford 1,258): B — Tesla POMP silently subsets to 365 observations, making Ford/Tesla comparison invalid (matches Human Issue #5)
- Finding 2 (POMP vs GARCH comparison invalid): B — POMP and GARCH log-likelihoods are incomparable; conclusion unsupported (matches Human Issue #5)
- Finding 3 (Bug in Tesla GARCH prediction plot): A — Ford's volatility used in Tesla's Figure 10 prediction bounds
- Finding 4 (R_n equation trivially equals 1): A — typographical error makes R_n = 1 identically; code correctly uses tanh
- Finding 5 (Ford global search missing file and wrong run_level): A — global search loads wrong file; run_level inconsistency
- Finding 6 (Ford and Tesla POMP at different computational scales): A — Tesla uses sequential %do% while Ford uses parallel %dopar%; different particle/iteration counts
- Finding 7 (POMP model description inconsistent with code): B — text writes Y_n = exp{H_n/2} without epsilon_n error term; code implements normal distribution (matches Human Issue #1)
- Finding 8 (Tesla POMP duplicates Apple figure captions): C — copy-paste captions referencing Apple stock mid-document
- Finding 9 (Incomplete sentence in introduction): D — unresolved parenthetical "(why we want to use log return instead of return?)" (matches Human Issue #9)
- Finding 10 (GARCH model selection inconsistently applied): C — t-GARCH table missing for Ford; selection criterion abandoned without justification
- Finding 11 (Weak identifiability rationalized without investigation): C — non-convergence of mu_h and H_0 dismissed without profile likelihood or reparameterization
- Finding 12 (Ford global search references wrong figure): C — text references Figure 12 but global convergence plot is Figure 14
- Finding 13 (Decomposition applied to log returns is questionable): C — classical decompose() misapplied to near-white-noise series
- Finding 14 (References section labeled "Scholarships"): C — section heading typo
- Finding 15 (YAML typo disables section numbering): C — nember_sections instead of number_sections

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "Tesla POMP uses a different dataset than Tesla GARCH, invalidating cross-model comparisons" and finding: "conclusion that POMP outperforms GARCH contradicted by Ford likelihoods")
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: covered (matched by finding: "incomplete parenthetical question '(why we want to use log return instead of return?)' left in final submission")

**Findings classification:**
- Finding 1 (Tesla POMP uses different dataset): B — Tesla POMP fitted to only 364 of 1,258 observations, making cross-model comparisons invalid (matches Human Issue #5)
- Finding 2 (POMP conclusion contradicted by Ford likelihoods): B — Ford GARCH achieves higher log-likelihood than POMP, directly contradicting the conclusion (matches Human Issue #5)
- Finding 3 (promised AIC comparison never delivered): A — three-way AIC comparison across ARIMA, GARCH, and POMP promised in introduction but absent
- Finding 4 (computation does not match reported methodology): A — Ford global search described as 100 replicates at 2,000 particles but saved .rda files show 20 replicates at 1,000 particles
- Finding 5 (no profile likelihoods): A — neither Ford nor Tesla POMP includes profile likelihood computations
- Finding 6 (leverage formula typographical error): A — numerator and denominator of R_n formula are identical, evaluating to 1 for all G_n
- Finding 7 (normal GARCH and t-GARCH likelihoods use different normalization): A — cross-table comparison potentially invalid due to different normalization conventions and effective sample sizes
- Finding 8 (Tesla prediction plot uses Ford forecast uncertainty): C — Figure 10 uses ford_ahead[,2] instead of tesla_ahead[,2] for prediction bands
- Finding 9 (Tesla POMP figure captions say "Apple"): C — chunk at line 751 labels Tesla figures as Apple; figure numbering restarts
- Finding 10 (Tesla POMP searches use sequential rather than parallel execution): C — Tesla uses %do% while Ford uses %dopar%, substantially increasing runtime
- Finding 11 (no benchmark comparison for POMP models): C — ARMA(0,0) not retained as baseline for POMP log-likelihood comparison
- Finding 12 (citation numbering inconsistent): C — Breto (2014) cited as [2] but [2] refers to a different source; Breto (2014) never listed
- Finding 13 (decomposition of log returns misinterpreted as meaningful trend): C — classical additive decomposition on near-white-noise returns does not reflect genuine price trends
- Finding 14 (phi search box overly narrow given bimodal behavior): C — phi restricted to (0.95, 0.99) may miss second mode visible in pair plots
- Finding 15 (incomplete parenthetical question left in submission): D — "(why we want to use log return instead of return?)" is an unresolved author note (matches Human Issue #9)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "Tesla POMP uses only last 365 observations; Ford uses all 1,258" and by finding: "Claim that 'POMP performs much better than GARCH' is not supported")
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: covered (matched by finding: "No model diagnostics specific to the POMP stochastic leverage model")
- Human Issue #9: covered (matched by finding: "Unresolved sentence fragment in introduction")

**Findings classification:**
- Major 1 (simulated-data benchmark): A — initial pfilter benchmark evaluated on simulated data, not real data
- Major 2 (Tesla 365 observations): B — Tesla POMP uses only last 365 observations while Ford uses all 1,258 (matches Human Issue #5)
- Major 3 (Tesla global IF2 initialization): A — Tesla global IF2 search incorrectly initialized from previous mif2 result object
- Major 4 (POMP vs GARCH claim unsupported): B — claim that "POMP performs much better than GARCH" is not supported by the likelihoods (matches Human Issue #5)
- Major 5 (non-convergence rationalized): A — non-convergence acknowledged but results interpreted as substantively meaningful
- Major 6 (no benchmark comparison): A — no quantitative goodness-of-fit comparison between POMP and a non-mechanistic baseline on the same dataset
- Major 7 (no profile likelihoods): A — no profile likelihoods or confidence intervals presented for any parameter
- Major 8 (particle count inadequate): A — particle count and computational settings inadequate for the Ford section; archived artifacts may not match described run level
- Minor (sentence fragment): D — unresolved parenthetical question in introduction not removed before submission (matches Human Issue #9)
- Minor (figure caption mismatch): C — Tesla section figures re-labeled "Figure 1" and "Figure 2" despite being 15th–18th figures in document
- Minor (wrong-dataset prediction): C — Tesla GARCH prediction confidence band uses Ford's predicted standard errors due to copy-paste error
- Minor (Tesla refers to Apple): C — Tesla section figure caption reads "Adjusted Closing Price of Apple" instead of Tesla
- Minor (ARMA not connected to GARCH): C — ARMA(0,0) conclusion not connected to motivation for GARCH via ARCH-effects test
- Minor (no POMP diagnostics): D — no simulated trajectories compared to observed log-returns to validate fitted POMP model (matches Human Issue #8)
- Minor (mu_h transformation): C — mu_h not log-transformed in partrans, allowing positive values during IF2 perturbation
- Minor (Breto citation): C — Breto (2014) credited in text but does not appear in reference list; reference [2] is course lecture notes

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: contradiction (AI says the model architecture — no separate measurement noise — is the correct Breto 2014 design; human says the model is missing a normal error)
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "M2 — Cross-model conclusion contradicted by paper's own numbers")
- Human Issue #6: covered (matched by finding: "m2 — ARMA AIC table absent from report body")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: covered (matched by finding: "m4 — Inline authoring note not removed")

**Findings classification:**
- M1: A — Baseline pfilter run on simulated data rather than actual returns, making reported log-likelihood improvement uninformative
- M2: B — Cross-model conclusion (POMP outperforms GARCH for both stocks) contradicted by paper's own numbers where Ford t-GARCH exceeds Ford POMP (matches Human Issue #5)
- M3: A — Tesla prediction figure uses Ford volatility bands due to variable naming error in code
- M4: A — No profile likelihoods or confidence intervals reported for any POMP parameter
- M5: F — AI says no separate measurement noise is the correct Breto (2014) architecture; human says the model is missing a normal error (contradicts Human Issue #1)
- m1: C — R_n formula typeset as identically 1 due to LaTeX transcription error; code correctly implements tanh(G_n)
- m2: D — ARMA AIC table absent from report body, only in supplementary Rmd (matches Human Issue #6)
- m3: C — Global search initializes from local search object rather than raw filter, potentially limiting exploration
- m4: D — Inline authoring note "(why we want to use log return instead of return?)" not removed from rendered document (matches Human Issue #9)
- m5: C — Ford uses 1000 particles vs Tesla's 2000 at run_level=3; uneven computational investment undiscussed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 3 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 1 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 4 | 5 | 6 | 3 |
| B (AI major, human also found) | 3 | 2 | 2 | 1 |
| C (AI minor, human missed) | 7 | 7 | 6 | 3 |
| D (AI minor, human also found) | 1 | 1 | 2 | 2 |
| E (Human found, AI missed) | 6 | 7 | 6 | 5 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 1 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 3 | 1 | 6 | 3/9 = 33% | 4 | 7 | 11/15 = 73% |
| Charlie | 2 | 1 | 7 | 2/9 = 22% | 5 | 7 | 12/15 = 80% |
| Doug | 2 | 2 | 6 | 3/9 = 33% | 6 | 6 | 12/16 = 75% |
| Evan | 1 | 2 | 5 | 3/8 = 38% | 3 | 3 | 6/9 = 67% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #2: Based on the GARCH analysis, one might try $\epsilon_n$ having a $t$ distribution rather than normal. The effective sample size plot also suggests that - there are some jumps that are large outliers under a normal model. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #3: A simpler stochastic volatility model might be worth trying before advancing to stochastic volatility with leverage. See Section 4 of https://ionides.github.io/531w22/final_project/project14/Blinded.html for an example. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #4: Conclusion: "improvements of log likelihood were not significant" moving from normal to t GARCH seems wrong - make a likelihood ratio test. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #7: "Other models with competitive AIC values are not invertible or causal, with polynomial roots inside of the unit circle" seems implausible, since `arima()` will never fit roots inside the unit circle, though they may be on the boundary or close to it. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 4 out of 9 human issues (44%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #1: Model is missing a normal error in the term $Y_n = \exp\{H_n/2\} \epsilon_n$. (Covered only by Alex)
- Human Issue #6: An AIC table for ARMA(p,q) is mentioned but not shown. (Covered only by Evan)
- Human Issue #8: Plotting simulations from the mechanistic models would allow us to visually assess the fitted models and compare the performance of the local to the global search. (Covered only by Doug)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 1 |
| Charlie | 0 |
| Doug | 1 |
| Evan | 1 |
