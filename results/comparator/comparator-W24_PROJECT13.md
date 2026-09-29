# Comparator Analysis — W24 Project 13

---

## Human Issues

1. There is too much R output, including unexplained warning messages.

2. Readers and writers may have many first languages, but we all have a commitment to being able to read and write in English for this course. In the context of this course, it is not reasonable to expect the reader to understand other languages.

3. The time plots would be more informative on a log scale. The sample ACF would also be more informative on the log of the data.

4. The three graphs at the beginning are confusing. They all have the same title, and it is not immediately obvious what the difference is between them (especially because the labels are not all in English). It would be helpful to either make this explicit in the plot titles or include some text clarifying this before the plots are shown.

5. Aggregating cases over weeks can be a good way to avoid interacting with the weekly reporting pattern. Otherwise, it has to be addressed explicitly in models or other data analysis of daily data.

6. Preferring `auto.arima` because it also does some other things, that may or may not be appropriate and are unexplained and presumably not understood by the group, is a problematic way to pick statistical methodology. Better to stick with a less sophisticated analysis that you fully understand.

7. The conclusions do not relate the ARIMA analysis to the POMP analysis. In fact, they don't discuss ARIMA at all, despite much of the report being spent on it. It would be good to compare log-likelihoods, though this requires care since the differencing when I>0 affects likelihood comparisons.

8. The ARIMA results are not always clear about which wave is under consideration. Results for the first wave have little relevance for the subsequent analysis.

9. The SARIMA code unfortunately sets `frequency=52` rather than `frequency=7` for 7 days in a week with daily data. The latter is the periodicity identified in the plots.

10. The fitted value plot for ARIMA can look over-optimistic, since even a simple model such as "predict day n by the data on day n-1" would look similarly good in this representation.

11. The report is right that the QQ-plot shows evidence of non-normality, but some of the comments in the discussion are incorrect. The report mentions that the QQ-plot could look like this because confirmed case data often does not follow a normal distribution. The QQ-plot is showing the distribution of the residuals, not the case data. This makes the following comment about using a Poisson or negative binomial model incorrect as well.

12. Less time spent on ARIMA would allow more attention to the mechanistic modeling, which ends up being more central to the conclusions.

13. In the local search results, the log-likelihood does not change much from the beginning of the particle filtering. This suggests the search is not improving the results much, which is corroborated by the parameters not changing much either throughout the run. Either running the local search for more iterations or choosing a different starting location is suggested. Because of this, the statement that most of the parameters converge is incorrect.

14. To evaluate the parameter estimates, it would be helpful to include a profile likelihood. This can help give a better idea if the parameters are accurately estimated. If this was omitted only because of lack of time, that should be mentioned.

15. Numbers and captions for figures would help the reader.

16. References should have name/title/year, e.g. APA format. All references should be cited in the text. The introduction has no references.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "SARIMA model mismatch + auto.arima justification is circular and unsupported")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: covered (matched by finding: "`ts()` frequency=52 misspecified for daily data")
- Human Issue #10: missed
- Human Issue #11: missed
- Human Issue #12: missed
- Human Issue #13: missed
- Human Issue #14: covered (matched by finding: "no likelihood profile or uncertainty quantification for any parameter")
- Human Issue #15: missed
- Human Issue #16: missed

**Findings classification:**
- Finding 1 (R-language step function syntax errors): A — R-language `siqriqr_step` has multiple rbinom calls with wrong argument count and references undefined variables
- Finding 2 (hard-coded absolute file path): A — Windows-specific absolute path prevents reproducibility
- Finding 3 (measurement model misspecified): A — accumulator H tracks recoveries rather than new detections, conflating recovery with confirmation
- Finding 4 (unexplained `e=100` intervention): A — hard-coded injection of 100 infectious individuals at day 125 is undocumented and unmotivated
- Finding 5 (parameters fixed without justification): A — `mu_QR_o`, `mu_QR_r`, `mu_QR_b`, `k` fixed in both searches without epidemiological rationale
- Finding 6 (`%do%` instead of `%dopar%`): A — local search runs sequentially while global search correctly uses parallel execution
- Finding 7 (global search filter too permissive): A — log-likelihood window of 1000 units is enormous and unreported
- Finding 8 (no likelihood profile): B — neither confidence intervals nor likelihood profiles reported for any parameter (matches Human Issue #14)
- Finding 9 (Beta/Omicron labeling inconsistency): A — compartments labeled Beta/Omicron inconsistently with scientific motivation and `R_b` listed twice
- Finding 10 (SARIMA model mismatch + auto.arima justification circular): B — authors say they use auto.arima because it considers other criteria but auto.arima also uses AIC by default; justification is unsupported (matches Human Issue #6)
- Finding 11 (`ts()` frequency=52 misspecified): D — `frequency=52` corresponds to weekly observations, not daily; correct value for weekly seasonality in daily data is 7 (matches Human Issue #9)
- Finding 12 (no post-fit simulation plots): C — only initial-guess simulations shown; no equivalent plots after local or global search
- Finding 13 (`Beta_or` ghost parameter): C — `Beta_or` appears in paramnames and rw.sd but is unused in the Csnippet
- Finding 14 ("WARIMA" label inconsistent): C — term "WARIMA" introduced informally and used interchangeably with SARIMA without formal definition
- Finding 15 (data re-downloaded from Google API): C — EDA section uses fragile API URL while POMP section uses local CSV; provenance of CSV unexplained

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 13 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1 (too much R output, unexplained warning messages): missed
- Human Issue #2 (non-English language in report): missed
- Human Issue #3 (time plots more informative on log scale; ACF on log of data): missed
- Human Issue #4 (three opening graphs confusing — same title, non-English labels): missed
- Human Issue #5 (aggregating cases over weeks avoids weekly reporting pattern): missed
- Human Issue #6 (uncritical reliance on auto.arima is problematic methodology): missed
- Human Issue #7 (conclusions don't relate ARIMA to POMP; no log-likelihood comparison): covered (matched by finding: "No quantitative benchmark comparison between SARIMA and POMP")
- Human Issue #8 (ARIMA results not clear about which wave; first-wave results have little relevance): missed
- Human Issue #9 (SARIMA code sets frequency=52 rather than frequency=7): covered (matched by finding: "Wrong seasonal frequency specification in ts() objects")
- Human Issue #10 (fitted value plot for ARIMA looks over-optimistic): missed
- Human Issue #11 (QQ-plot comment incorrect — shows residuals, not case data; Poisson/NB comment also incorrect): missed
- Human Issue #12 (less time on ARIMA would allow more attention to mechanistic modeling): missed
- Human Issue #13 (local search log-likelihood barely changes; search not improving; convergence claim incorrect): covered (matched by finding: "No convergence diagnostics for global search; eta instability unresolved")
- Human Issue #14 (profile likelihood would help evaluate parameter estimates): covered (matched by finding: "No profile likelihoods or confidence intervals")
- Human Issue #15 (figure numbers and captions missing): missed
- Human Issue #16 (references lack name/title/year; not cited in text; introduction has no references): missed

**Findings classification:**
- Major-1 (force of infection driven by quarantined rather than infectious compartments): A — fundamental rprocess specification error, no human issue raised this
- Major-2 (accumulator H tracks Q→R recoveries rather than I→Q case detections): A — systematic measurement mismatch, no human issue raised this
- Major-3 (hard-coded local Windows file path makes POMP analysis non-reproducible): A — reproducibility failure, no human issue raised this
- Major-4 (undocumented ad-hoc event injection of 100 individuals at t=125): A — unjustified latent-state manipulation, no human issue raised this
- Major-5 (no profile likelihoods or confidence intervals): B — matches Human Issue #14
- Major-6 (wrong seasonal frequency: frequency=52 instead of frequency=7): B — matches Human Issue #9
- Major-7 (no quantitative benchmark comparison between SARIMA and POMP): B — matches Human Issue #7
- Major-8 (broken R-language rprocess prototype with multiple errors): A — code correctness issue, no human issue raised this
- Major-9 (unused parameters Beta_or and mu_QR_r in paramnames inflate complexity): A — no human issue raised this
- Major-10 (no convergence diagnostics for global search; eta instability unresolved): B — matches Human Issue #13
- Minor-1 (AIC table uses non-seasonal orders not comparable to auto.arima result): C — no human issue raised this specific point
- Minor-2 (no residual ACF plot for either SARIMA model): C — no human issue raised this
- Minor-3 (compartment description has two R_b entries, omits R_o; copy-paste error): C — no human issue raised this
- Minor-4 (causal language used without causal identification strategy): C — no human issue raised this
- Minor-5 (typos: "fous", "dtrains", "acll", "Futhermore"): C — no human issue raised this
- Minor-6 (no sessionInfo() or package version documentation): C — no human issue raised this
- Minor-7 (initial condition places 100 in Q_o at t=0 without justification): C — no human issue raised this

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 4 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 12 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "No quantitative comparison between SARIMA and POMP models"; also matched by finding: "No benchmark comparison between the POMP model and a non-mechanistic statistical model")
- Human Issue #8: missed
- Human Issue #9: covered (matched by finding: "SARIMA period misspecification — frequency=52 instead of frequency=7")
- Human Issue #10: missed
- Human Issue #11: missed
- Human Issue #12: missed
- Human Issue #13: covered (matched by finding: "Insufficient computational effort — log-likelihood and parameters not improving, convergence claims incorrect")
- Human Issue #14: covered (matched by finding: "No profile likelihoods or confidence intervals for any parameter")
- Human Issue #15: missed
- Human Issue #16: missed

**Findings classification:**
- Finding 1 (No quantitative comparison between SARIMA and POMP): B — no quantitative ARIMA-to-POMP comparison provided (matches Human Issue #7)
- Finding 2 (Broken R-code step function with undefined variables): A — plain-R siqriqr_step has missing n=1, undefined dt, undefined dN_SE variables, and no return value
- Finding 3 (Hard-coded absolute path breaks reproducibility): A — Windows-specific absolute path in read_csv prevents execution on any other system
- Finding 4 (No profile likelihoods or confidence intervals): B — neither local nor global search reports profile likelihoods; no uncertainty attached to estimates (matches Human Issue #14)
- Finding 5 (Insufficient computational effort — Nmif=50, Np=2000, 50 replicates): B — convergence traces show non-convergence; claim that "most parameters converge" is incorrect (matches Human Issue #13)
- Finding 6 (SARIMA period misspecification — frequency=52 instead of frequency=7): B — daily data with 7-day cycle coded as frequency=52, inconsistent with ACF evidence (matches Human Issue #9)
- Finding 7 (Accumulator H tracks recoveries not quarantine entries): A — measurement model links observations to H accumulating Q-exits rather than Q-entries, distorting rho and transition rate estimates
- Finding 8 (No benchmark comparison between POMP and non-mechanistic model): B — SARIMA and POMP likelihoods never placed side by side; comparison only visual (matches Human Issue #7)
- Finding 9 (Model diagnostic checks absent): A — no conditional log-likelihood plots, ESS traces, or simulated vs. observed summary statistics
- Finding 10 (Beta_or in paramnames but unused in Csnippet): A — orphaned parameter wastes computational degrees of freedom and contributes to apparent non-convergence
- Finding 11 (Confusion about which strains are modeled): C — model labels O/B but narrative describes Delta/Omicron; compartment naming inconsistent with epidemiological narrative
- Finding 12 (%do% instead of %dopar% for local search): C — serial execution for 20 replicate chains increases compute time and reduces feasibility of additional iterations
- Finding 13 (AIC table uses non-seasonal ARIMA, not SARIMA): C — AIC table fits plain ARIMA(p,1,q) without seasonal component, making comparison with auto.arima's seasonal suggestion non-comparable
- Finding 14 (No reported log-likelihood values in prose): C — best log-likelihood from both searches never quoted in text; comparison claim unsupported
- Finding 15 (Typographical and notational errors): C — multiple typos and inconsistent parameter notation in model description

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 5 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 12 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "AIC table minimum vs auto.arima choice not reconciled")
- Human Issue #7: covered (matched by finding: "No benchmark comparison between POMP and SARIMA")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed
- Human Issue #11: missed
- Human Issue #12: missed
- Human Issue #13: covered (matched by finding: "Non-convergent mif2 traces")
- Human Issue #14: covered (matched by finding: "No profile likelihoods or parameter uncertainty")
- Human Issue #15: missed
- Human Issue #16: missed

**Findings classification:**
- 24.13.1: A — Transmission force driven by quarantined rather than infectious individuals
- 24.13.2: A — Undisclosed hard-coded perturbation of 100 individuals injected at t=125
- 24.13.3: B — No benchmark comparison between POMP and SARIMA (matches Human Issue #7)
- 24.13.4: B — No profile likelihoods or parameter uncertainty reported (matches Human Issue #14)
- 24.13.5: B — Non-convergent mif2 traces; parameters and loglik not plateauing (matches Human Issue #13)
- 24.13.6: C — Fixed parameters used throughout searches without epidemiological justification
- 24.13.7: C — Code inconsistency between R prototype and Csnippet (undefined variables in prototype)
- 24.13.8: C — Severe Monte Carlo variability (loglik.se as high as 89.3) for some parameter sets
- 24.13.M1: C — No ESS diagnostics to assess particle filter degeneracy
- 24.13.M2: C — rho search range constrained to [0.4, 0.6] without justification
- 24.13.M3: C — Biologically inconsistent initial conditions (Q_o=100 with I_o=0)
- 24.13.9: D — AIC table optimum differs from auto.arima recommendation without reconciliation (matches Human Issue #6)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 2 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 12 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 8 | 6 | 5 | 2 |
| B (AI major, human also found) | 2 | 4 | 5 | 3 |
| C (AI minor, human missed) | 4 | 7 | 5 | 6 |
| D (AI minor, human also found) | 1 | 0 | 0 | 1 |
| E (Human found, AI missed) | 13 | 12 | 12 | 12 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 2 | 1 | 13 | 3/16 = 19% | 8 | 4 | 12/15 = 80% |
| Charlie | 4 | 0 | 12 | 4/16 = 25% | 6 | 7 | 13/17 = 76% |
| Doug | 5 | 0 | 12 | 4/16 = 25% | 5 | 5 | 10/15 = 67% |
| Evan | 3 | 1 | 12 | 4/16 = 25% | 2 | 6 | 8/12 = 67% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #1: There is too much R output, including unexplained warning messages. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #2: Readers and writers may have many first languages, but we all have a commitment to being able to read and write in English for this course. In the context of this course, it is not reasonable to expect the reader to understand other languages. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #3: The time plots would be more informative on a log scale. The sample ACF would also be more informative on the log of the data. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #4: The three graphs at the beginning are confusing. They all have the same title, and it is not immediately obvious what the difference is between them (especially because the labels are not all in English). It would be helpful to either make this explicit in the plot titles or include some text clarifying this before the plots are shown. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #5: Aggregating cases over weeks can be a good way to avoid interacting with the weekly reporting pattern. Otherwise, it has to be addressed explicitly in models or other data analysis of daily data. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #8: The ARIMA results are not always clear about which wave is under consideration. Results for the first wave have little relevance for the subsequent analysis. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #10: The fitted value plot for ARIMA can look over-optimistic, since even a simple model such as "predict day n by the data on day n-1" would look similarly good in this representation. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #11: The report is right that the QQ-plot shows evidence of non-normality, but some of the comments in the discussion are incorrect. The report mentions that the QQ-plot could look like this because confirmed case data often does not follow a normal distribution. The QQ-plot is showing the distribution of the residuals, not the case data. This makes the following comment about using a Poisson or negative binomial model incorrect as well. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #12: Less time spent on ARIMA would allow more attention to the mechanistic modeling, which ends up being more central to the conclusions. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #15: Numbers and captions for figures would help the reader. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #16: References should have name/title/year, e.g. APA format. All references should be cited in the text. The introduction has no references. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 11 out of 16 human issues (69%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

(none)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |
