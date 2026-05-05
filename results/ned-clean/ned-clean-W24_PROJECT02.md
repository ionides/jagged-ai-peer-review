# Ned-Clean Analysis — W24 Project 02

---

## Human Issues

1. Explain acronyms at first occurrence, e.g., CPUE.
2. The alternative prey hypothesis (mentioned in the project title) could be explained in the introduction. It becomes clearer later on, in the model section.
3. The description of what is denoted by 'peak_rodent_year' was lacking — it only says "Peak rodent year is scored as 'yes', otherwise 'no'" without explaining what is meant by that or how/when it is decided.
4. It could have been explicitly explained why the log of CPUE was used in the model instead of the CPUE itself.
5. ARIMA with differencing parameter I>0 does not have immediately comparable likelihood, so is not appropriate as a benchmark. One could use ARMA with a trend instead.
6. If the formal null and alternative hypotheses are defined for the KPSS test, it may be clearer what can legitimately be concluded from it.
7. The log-likelihood search is incomplete, as evidenced by the local search beating the preliminary global search.
8. In Fig 3.1, the effective sample size is usually 1, and never more than 2.2, indicating serious particle depletion (Np=50 is insufficient, and model improvements may be needed).
9. Diagnostic plot: the starting point has very low likelihood; a search starting from a better place might be easier.
10. It is premature to conclude that "ARMA is a better fit to the data" given the preliminary nature of the mechanistic model.
11. There is a mismatch between the text-reported log-likelihood (-205) and the value in the R output (-288).

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "ARIMA/POMP comparison invalid — different observation scales and differencing")
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "Global search range extremely narrow and biologically unmotivated")
- Human Issue #8: covered (matched by finding: "Particle filter uses Np=5 for likelihood evaluation after mif2")
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "ARIMA/POMP comparison invalid — conclusion that ARMA fits better is not validly supported")
- Human Issue #11: missed

**Findings classification:**
- Major #1 (POMP log-likelihood worse than ARIMA, invalid comparison, unsupported conclusion): B — matches Human Issues #5 and #10
- Major #2 (Fox population latent state with no data — model unidentifiable): A
- Major #3 (Particle filter uses Np=5 for likelihood evaluation): B — matches Human Issue #8
- Major #4 (Same noise W_t^F applied to both fox and bird equations): A
- Major #5 (Negative binomial stated but normal distribution implemented): A
- Major #6 (obs_names argument invalid — logCPUE removed from pomp object): A
- Major #7 (Global search range extremely narrow, biologically unmotivated, fixed_params duplication): B — matches Human Issue #7
- Major #8 (Convergence diagnostics as static images with absolute local file paths): A
- Minor #9 (Parameter transformation applies log to params that can be negative or zero): C
- Minor #10 (logRho parameter naming and use confused): C
- Minor #11 (ARIMA model selection label error — wrong figure reference): C
- Minor #12 (Only 2 rows in bird_params_middle.csv — global search nearly failed): C
- Minor #13 (No profile likelihood or confidence intervals): C
- Minor #14 (dt=1/52 step size not justified): C
- Minor #15 (Bibliography file path hardcoded to absolute local path): C

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

Human issues covered: #5, #7, #8, #10 (4 of 11)

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "Invalid ARIMA vs POMP log-likelihood comparison")
- Human Issue #6: covered (matched by finding: "KPSS test p-value truncation — misstatement of null hypothesis semantics")
- Human Issue #7: covered (matched by finding: "Global search critically underpowered — only 2 valid results in the CSV")
- Human Issue #8: covered (matched by finding: "Particle count too small, Np=5 in one key evaluation")
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "Invalid ARIMA vs POMP log-likelihood comparison — conclusion unsupported")
- Human Issue #11: missed

**Findings classification:**
- Major #1 (Invalid ARIMA vs POMP log-likelihood comparison): B — matches Human Issues #5 and #10
- Major #2 (Global search critically underpowered — only 2 valid results): B — matches Human Issue #7
- Major #3 (Particle count too small, Np=5): B — matches Human Issue #8
- Major #4 (No profile likelihoods, parameter identifiability unassessed): A
- Major #5 (Bird equation uses same noise term as fox equation): A
- Major #6 (Measurement model states wrong distribution — NB vs Normal): A
- Major #7 (Global search parameter space disconnected from local search results): A
- Major #8 (IF2 convergence not demonstrated, only 50 iterations): A
- Minor #1 (Bibliography hard-coded to local path): C
- Minor #2 (Data path also hard-coded): C
- Minor #3 (Q_fit_bird_local_mifs.rds contains extra parameters not in Rmd): C
- Minor #4 (ARMA and POMP log-likelihoods not on same scale): C (human issue #5 already covered by Major #1)
- Minor #5 (eval=FALSE on global search chunk, results not generated from Rmd): C
- Minor #6 (KPSS test p-value truncation — misstatement of null hypothesis): D — matches Human Issue #6
- Minor #7 (Parameter gamma could produce negative predation rates): C
- Minor #8 (No simulation-based model validation): C
- Minor #9 (ACF section cross-reference error): C
- Minor #10 (Missing sessionInfo() and package version documentation): C
- Minor #11 (Rodent covariate treated as known without uncertainty): C
- Minor #12 (Species name misspelling): C

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 11 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

Human issues covered: #5, #6, #7, #8, #10 (5 of 11)

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "Invalid ARIMA vs POMP log-likelihood comparison")
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "Global search severely underperforms local search — box misalignment and structural flaws")
- Human Issue #8: covered (matched by finding: "Critically inadequate particle count for log-likelihood evaluation, Np=5")
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "Invalid ARIMA vs POMP log-likelihood comparison — conclusion unsupported")
- Human Issue #11: missed

**Findings classification:**
- Major #1 (Invalid ARIMA vs POMP log-likelihood comparison): B — matches Human Issues #5 and #10
- Major #2 (Critically inadequate particle count, Np=5): B — matches Human Issue #8
- Major #3 (Global search severely underperforms local search): B — matches Human Issue #7
- Major #4 (Measurement model text-code inconsistency — NB vs Normal): A
- Major #5 (No parameter identifiability assessment or confidence intervals): A
- Major #6 (No model diagnostics at fitted MLE): A
- Major #7 (Partial convergence evidence, inadequate optimization): A
- Minor bullet 1 (PACF caption reads "ACF of logCPUE"): C
- Minor bullet 2 (Body text references wrong figure for PACF): C
- Minor bullet 3 ("Lotka-Volterra" misspelled throughout): C
- Minor bullet 4 (Typo "he log-likelihood"): C
- Minor bullet 5 (Species name misspelling — Lapagos): C
- Minor bullet 6 (logF_0=1 text vs logB_0=1 code inconsistency): C
- Minor bullet 7 (W_t^F notation used for both equations — notation/code mismatch): C
- Minor bullet 8 (Global search stores to different CSV names): C
- Minor bullet 9 (No discussion of log-scale SDE justification): C
- Minor bullet 10 (partrans applies log to already-log-scale parameters): C

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 10 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

Human issues covered: #5, #7, #8, #10 (4 of 11)

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "Invalid ARIMA vs POMP log-likelihood comparison")
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "Global search worse than local search")
- Human Issue #8: covered (matched by finding: "mif2 likelihoods reported without replicated pfilter — SE ~31 log units")
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "Invalid ARIMA vs POMP log-likelihood comparison — conclusion unsupported")
- Human Issue #11: covered (matched by finding: "mif2 likelihoods reported — shown output est: -288.64 vs reported -205")

**Findings classification:**
- Point 24.02.1 (Invalid ARIMA vs POMP log-likelihood comparison): B — matches Human Issues #5 and #10
- Point 24.02.2 (mif2 likelihoods reported without replicated pfilter): B — matches Human Issues #8 and #11
- Point 24.02.4 (Convergence inadequately demonstrated): A
- Point 24.02.3 (No profile likelihoods or confidence intervals): A
- Point 24.02.5 (Global search worse than local search): B — matches Human Issue #7
- Point 24.02.6 (Measurement model noise structure and logRho scale): C
- Point 24.02.7 (Inconsistent notation — log.CPUE vs logCPUE): C
- Point 24.02.8 (Figure caption error — ACF labeled as PACF): C
- Point 24.02.11 (ARIMA residuals not validated): C
- Point 24.02.13 (No parameter estimate table): C
- Point 24.02.15 (AIC table inconsistency): C

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 2 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

Human issues covered: #5, #7, #8, #10, #11 (5 of 11)

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 5 | 5 | 4 | 2 |
| B (AI major, human also found) | 3 | 3 | 3 | 3 |
| C (AI minor, human missed) | 7 | 11 | 10 | 6 |
| D (AI minor, human also found) | 0 | 1 | 0 | 0 |
| E (Human found, AI missed) | 7 | 6 | 7 | 6 |

---

## Per-Reviewer Metrics

Note: Human Recall and AI-Unique Rate are computed using AI-finding counts (B, D) and human-issue coverage counts where one AI finding may cover multiple human issues. Human Recall uses the count of distinct human issues covered.

| Reviewer | Human issues covered | E (missed) | Human Recall | A+C (AI-unique) | A+B+C+D (total AI) | AI-Unique Rate |
|----------|--------------------:|----------:|-------------:|----------------:|-------------------:|---------------:|
| Alex | 4 | 7 | 4/11 = 36% | 12 | 15 | 12/15 = 80% |
| Charlie | 5 | 6 | 5/11 = 45% | 16 | 20 | 16/20 = 80% |
| Doug | 4 | 7 | 4/11 = 36% | 14 | 17 | 14/17 = 82% |
| Evan | 5 | 6 | 5/11 = 45% | 8 | 11 | 8/11 = 73% |

Human Recall = (human issues covered) / 11
AI-Unique Rate = (A + C) / (A + B + C + D)

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Issue #1: Explain acronyms at first occurrence (e.g., CPUE) — missed by all 4 reviewers
- Issue #2: Alternative prey hypothesis not explained in the introduction — missed by all 4 reviewers
- Issue #3: Description of 'peak_rodent_year' is lacking — missed by all 4 reviewers
- Issue #4: Why log of CPUE is used instead of CPUE itself not explained — missed by all 4 reviewers
- Issue #6: KPSS test null and alternative hypotheses not defined (Charlie partially addressed the misinterpretation) — missed by Alex, Doug, and Evan; partially addressed by Charlie (D)
- Issue #9: Diagnostic plot starting point has very low likelihood; suggestion to start from better place — missed by all 4 reviewers

Strict consensus misses (missed by ALL 4 reviewers): #1, #2, #3, #4, #9 — 5 out of 11 (45%)

Issue #6 was covered by Charlie (D) but missed by Alex, Doug, and Evan.

### Unique finds per reviewer

Issues covered by exactly one reviewer (and missed by all others):

- Issue #6 (KPSS null/alternative hypotheses): covered only by Charlie (Minor #6)
- Issue #11 (text -205 vs R output -288 mismatch): covered only by Evan (Point 24.02.2)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 1 (Issue #6) |
| Doug | 0 |
| Evan | 1 (Issue #11) |

### Universal AI-only flags

Issues raised by every reviewer that the human did not mention (must appear in all four reviewers as A or B/D matching a non-human issue):

The following concerns were raised as Major findings by all four reviewers and were not in the human issues list:

1. **No profile likelihoods or confidence intervals for any parameter** — flagged as Major by Alex (#13 is Minor, wait — checking: Alex classifies this as Minor #13; Charlie as Major #4; Doug as Major #5; Evan as Major 24.02.3). Not unanimous as Major but raised by all four as A/C.

2. **Measurement model text-code inconsistency (Negative Binomial stated, Normal implemented)** — flagged by Alex (Major #5, A), Charlie (Major #6, A), Doug (Major #4, A). Evan does not explicitly flag the NB vs Normal inconsistency as a separate point — Evan's Point 24.02.6 touches measurement model noise structure but not the NB/Normal mismatch directly. So this is raised by 3 of 4 reviewers (Alex, Charlie, Doug) but not Evan.

Genuine universal AI-only flags (raised by all 4 reviewers, not in human list):
- **Convergence not adequately demonstrated / IF2 non-convergence**: Alex Major #8 (static images, non-reproducible), Charlie Major #8 (only 50 iterations, non-convergence), Doug Major #7 (partial convergence, inadequate optimization), Evan Major 24.02.4 (convergence inadequately demonstrated). All 4 raise this. Not in human issues. Universal AI-only flag. Count: 1.

Note: The human's Issue #7 (local beating global = incomplete search) is related to convergence but is specifically about the search incompleteness, not the IF2 trace convergence. These are distinct enough that the convergence finding is genuinely AI-unique.

Universal AI-only flags count: 1 (convergence inadequately demonstrated / IF2 non-convergence of key parameters)
