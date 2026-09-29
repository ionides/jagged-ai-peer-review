# Comparator Analysis — W21 Project 10

---

## Human Issues

1. There is an erroneous instantaneous drop in susceptibles evident when this is plotted. It later becomes clear that this corresponds to a huge spike in cases. A referee noticed the following: I try to search for the news about this abnormality but cannot get a clear answer. Instead, I find a piece of news that could help to explain it. According to FOX 5 Atlanta Digital Team, "The spike in cases is also a spike in reported tests. The Georgia Department of Public Health said about 12,000 of the cases reported today are all from one facility in metro Atlanta that is catching up on reporting its numbers for the week." Therefore one probably the solution is to delete it and fill it with the mean of adjacent day's cases, which is a common method I have seen to solve this kind of problem in some paper.

2. How much benefit is there to develop a range of models for vaccination counts when the main subsequent goal is to use that as a covariate to understand cases, for which vaccination is treated as an input not a response. The goal behind looking at both these time series is not clearly explained.

3. There is a clear outlier in the cases - it is unclear what was done about it. Diagnostic plots are not shown, but potentially such an outlier can be problematic for model development and fitting.

4. Too many significant figures in the table. For example, 3 significant figures, or 1 decimal place for log likelihood, is usually enough.

5. The ARMA(4,1,4) model for vaccination seems to successfully describe the weekly periodicity.

6. Why do we not see the covariate of vaccination helping to explain the 2nd difference of COVID cases? It may be because the covariate is not influencing COVID at this timescale - a second difference is somewhat like a second derivative.

7. The project did not get so far into the POMP modeling. The simulated models have far less variability than the data, which likely explains why they cannot provide a statistical fit. Modeling multiple COVID waves is not easy: see Projects 13 and 15 for successful approaches.

8. The graphic in the introduction contains microbiological details that are not needed for the project. Either explain the role of this information, or leave it out.

9. Non-English captions on some graphs were distracting to some readers, as were other typos and inconsistent abbreviations.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "No Likelihood-Based Inference Performed for Any POMP Model"; also matched by finding: "No Parameter Estimation — All Parameters Are Hand-Tuned")
- Human Issue #8: missed
- Human Issue #9: missed

**Findings classification:**
- Finding 1 (No Likelihood-Based Inference for POMP): B — no particle filter run, no likelihood reported, no inferential content (matches Human Issue #7)
- Finding 2 (No Parameter Estimation — All Parameters Hand-Tuned): B — no mif2 local/global search, no profile likelihood (matches Human Issue #7)
- Finding 3 (Bug in Model 3: N_SV Drawn from I Instead of S): A — mathematical writeup has vaccination transition drawing from infectious compartment rather than susceptible
- Finding 4 (Binomial Measurement Model Source of -Inf Log-Likelihoods): A — dbinom called with non-integer H causing -Inf, unresolved in main body
- Finding 5 (Data Window Choice Unexplained): A — 105-day subset of 413-observation series not epidemiologically motivated
- Finding 6 (Duplicate Introduction Section Content): A — two paragraphs in Section 2.1 are verbatim copies of Section 1 text
- Finding 7 (LRT Degrees of Freedom Are Wrong): A — pchisq uses df=2 but ARIMA(4,1,4) vs ARIMA(1,1,1) difference is 6 parameters
- Finding 8 (ARMA Model Uses Wrong Data Split): A — pre-vaccination ARIMA coefficients applied to post-vaccination data without re-estimation
- Finding 9 (Susceptible Population Calculation Conflates Cumulative Cases with Active Immunity): C — deaths double-counted via both cases and deaths terms in susceptible formula
- Finding 10 (Vaccination Rate Hard-Coded in Models 1 and 2): C — fixed constant embedded in Csnippet with no corresponding estimable parameter
- Finding 11 (Model 2 Uses index as State Variable Incorrectly): C — deterministic time counter declared as stochastic state, wastes memory in particle filtering
- Finding 12 (Quadratic Vaccination Fit Without Residual Diagnostics): C — no residual plots, normality check, or ACF of residuals for the quadratic model
- Finding 13 (AIC Table Search Reaches Upper Boundary Without Expanding): C — AR5/MA5 optimal at boundary but grid not expanded; ARIMA(4,1,4) selection not formally justified
- Finding 14 (No Diagnostics for ARIMA Models): C — no ACF/PACF of residuals, no Ljung-Box test, no normality checks for any fitted ARIMA
- Finding 15 (Live URL Data Downloads Create Reproducibility Risk): C — main code blocks pull from live GitHub URLs rather than local CSV files

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: covered (matched by findings: "no likelihood-based inference performed on any POMP model"; "no convergence diagnostics, no mif2 runs in main analysis"; "no quantitative goodness-of-fit statistics reported for any model")
- Human Issue #8: missed
- Human Issue #9: missed

**Findings classification:**
- Finding 1 (No likelihood-based inference on any POMP model): B — no likelihood maximization performed; all parameters hand-selected; pfilter/mif2 abandoned (matches Human Issue #7)
- Finding 2 (No convergence diagnostics, no mif2 runs): B — main analysis has no iterated filtering runs or likelihood traces (matches Human Issue #7)
- Finding 3 (Smoothed non-integer data fed to binomial measurement model): A — 7-day rolling mean produces non-integer values passed to dbinom, causing undefined or silently wrong likelihood
- Finding 4 (Model 3 math inconsistent with code): A — equations specify binomial draw from I but code draws from S
- Finding 5 (LRT uses wrong df and mismatched data): A — ARIMA(4,1,4) vs ARIMA(1,1,1) tested with df=2 instead of df=6; LRT applied to different series than AIC table
- Finding 6 (No quantitative goodness-of-fit statistics for any SEIR variant): B — model comparison done entirely by visual inspection (matches Human Issue #7)
- Finding 7 (No benchmark comparison for POMP model): A — no non-mechanistic benchmark compared against SEIR using a common quantitative metric
- Finding 8 (H accumulator tracks recoveries, compared to new case reports): A — dN_IR used as basis for reported case counts, but reports measure new positive tests
- Finding 9 (Data duplication in introduction and Section 2.1): C — identical paragraphs about data sources appear in both sections
- Finding 10 (Vaccine constant V applied per Euler substep, not per day): C — V=2500 per substep yields 20,000 vaccinations/day with 8 substeps; hard-coded, not estimated
- Finding 11 (No residual diagnostics for ARIMA models): C — ACF/PACF of residuals and Ljung-Box test absent for both ARIMA models
- Finding 12 (Model selection ignores upper-boundary issue in AIC table): C — AR5/MA5 discarded without extending search to verify optimum is not at boundary
- Finding 13 (ARIMA model applied to post-vaccination data after pre-vaccination selection): C — no justification that pre-vaccination ARIMA structure persists; vaccination covariate coefficient reported as very small with no hypothesis test
- Finding 14 (Inconsistent parameter values between text and equations): C — text states mu_IR=0.9 but code uses mu_IR=0.09
- Finding 15 (Data loaded from live external URLs without local backup): C — reproducibility risk if GitHub URLs become unavailable

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 8 |
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
- Human Issue #7: covered (matched by findings: "No Likelihood-Based Inference Performed" and "Visual-Only Goodness-of-Fit Assessment")
- Human Issue #8: missed
- Human Issue #9: missed

**Findings classification:**
- Major 1 (No Likelihood-Based Inference Performed): B — particle filter produced degenerate likelihoods, POMP analysis could not achieve its primary goal (matches Human Issue #7)
- Major 2 (Binomial Measurement Model Causes Degenerate Likelihood): A — specific technical root cause of degenerate particle filter not raised by humans
- Major 3 (Visual-Only Goodness-of-Fit Assessment): B — all models assessed purely by visual comparison with no quantitative fit statistics (matches Human Issue #7)
- Major 4 (Vaccination Subtraction Can Drive S Below Zero): A — critical structural bug allowing negative susceptible counts not raised by humans
- Major 5 (Model 3 Vaccination Rate Draws From Wrong Compartment): A — equation–code discrepancy using I instead of S as base for vaccination not raised by humans
- Major 6 (No Benchmark Comparison for POMP Model): A — no ARMA or other non-mechanistic benchmark compared against POMP models not raised by humans
- Major 7 (LRT Applied to Mismatched Models with Wrong Degrees of Freedom): A — invalid LRT comparing models on different outcomes with incorrect df not raised by humans
- Major 8 (No Parameter Identifiability Assessment): A — no profile likelihoods or confidence intervals computed not raised by humans
- Major 9 (POMP Applied to Rolling-Mean Data, Misspecified Measurement Model): A — rolling mean creates autocorrelated non-integer observations incompatible with binomial model not raised by humans
- Major 10 (index State Variable / Linear Vaccination Term Unbounded): A — hardcoded slope and unbounded linear vaccination term precludes optimization not raised by humans
- Minor: Data loading from external URLs: C — reproducibility dependent on external URL stability not raised by humans
- Minor: mu_IR not declared in partrans: C — missing log transform for mu_IR in parameter transformation not raised by humans
- Minor: Section 2.1 and Introduction duplicated: C — verbatim repetition of data description not raised by humans
- Minor: N population values inconsistent across models: C — small discrepancies in N across Models 1–3 not raised by humans
- Minor: No random seeds for reproducibility: C — stochastic computations not seeded for reproducibility not raised by humans
- Minor: Susceptible population formula double-counts recoveries: C — EDA formula may double-subtract deaths through cases column not raised by humans
- Minor: No convergence traces or ESS diagnostics: C — particle filter diagnostic plots not included in rendered document not raised by humans
- Minor: References use raw URLs rather than formal citations: C — bibliographic entries are bare URLs not raised by humans

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "No likelihood-based inference performed"; also matched by finding: "Forward simulations are not goodness-of-fit evidence")
- Human Issue #8: missed
- Human Issue #9: missed

**Findings classification:**
- ID 21.10.8 (No likelihood-based inference): B — All POMP models parameterized by hand with no mif2 or pfilter log-likelihood reported (matches Human Issue #7)
- ID 21.10.1/21.10.3 (Measurement model -Inf likelihoods): A — dmeas uses dbinom with H as size causing -Inf likelihoods; dnbinom fix in appendix also incorrect
- ID 21.10.2 (Model 3 compartment error): A — dN_SV vaccination drawn from I instead of S, invalidating Model 3
- ID 21.10.9 (No benchmark comparison): A — ARMA analysis targets vaccination counts while POMP targets cases; no quantitative comparison on the same outcome
- Forward simulations finding (unnamed): B — Forward simulations from hand-tuned parameters presented as evidence of model fit but are not conditioning on observations (matches Human Issue #7)
- ID 21.10.5 (LRT degrees of freedom): C — Chi-squared test stated with 2 d.f. but parameter count difference is 6
- ID 21.10.3 (mu_EI/mu_IR unit confusion): C — mu_EI = 13 stated as rate implies 1.8-hour latent period; inconsistent text values for mu_IR
- Duplicate text (unnamed): C — Two full paragraphs on data sources appear verbatim in both Introduction and Section 2.1
- Missing figure captions (unnamed): C — Most figures lack descriptive captions
- RNG seeds (unnamed): C — set.seed not applied consistently across all stochastic operations

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 6 | 5 | 8 | 3 |
| B (AI major, human also found) | 2 | 3 | 2 | 2 |
| C (AI minor, human missed) | 7 | 7 | 8 | 5 |
| D (AI minor, human also found) | 0 | 0 | 0 | 0 |
| E (Human found, AI missed) | 8 | 8 | 8 | 8 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 2 | 0 | 8 | 1/9 = 11% | 6 | 7 | 13/15 = 87% |
| Charlie | 3 | 0 | 8 | 1/9 = 11% | 5 | 7 | 12/15 = 80% |
| Doug | 2 | 0 | 8 | 1/9 = 11% | 8 | 8 | 16/18 = 89% |
| Evan | 2 | 0 | 8 | 1/9 = 11% | 3 | 5 | 8/10 = 80% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #1: There is an erroneous instantaneous drop in susceptibles evident when this is plotted. It later becomes clear that this corresponds to a huge spike in cases. A referee noticed the following: I try to search for the news about this abnormality but cannot get a clear answer. Instead, I find a piece of news that could help to explain it. According to FOX 5 Atlanta Digital Team, "The spike in cases is also a spike in reported tests. The Georgia Department of Public Health said about 12,000 of the cases reported today are all from one facility in metro Atlanta that is catching up on reporting its numbers for the week." Therefore one probably the solution is to delete it and fill it with the mean of adjacent day's cases, which is a common method I have seen to solve this kind of problem in some paper. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #2: How much benefit is there to develop a range of models for vaccination counts when the main subsequent goal is to use that as a covariate to understand cases, for which vaccination is treated as an input not a response. The goal behind looking at both these time series is not clearly explained. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #3: There is a clear outlier in the cases - it is unclear what was done about it. Diagnostic plots are not shown, but potentially such an outlier can be problematic for model development and fitting. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #4: Too many significant figures in the table. For example, 3 significant figures, or 1 decimal place for log likelihood, is usually enough. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #5: The ARMA(4,1,4) model for vaccination seems to successfully describe the weekly periodicity. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #6: Why do we not see the covariate of vaccination helping to explain the 2nd difference of COVID cases? It may be because the covariate is not influencing COVID at this timescale - a second difference is somewhat like a second derivative. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #8: The graphic in the introduction contains microbiological details that are not needed for the project. Either explain the role of this information, or leave it out. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #9: Non-English captions on some graphs were distracting to some readers, as were other typos and inconsistent abbreviations. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 8 out of 9 human issues (89%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

(none)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |
