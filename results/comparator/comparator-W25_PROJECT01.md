# Comparator Analysis — W25 Project 01

---

## Human Issues

1. $k$ could be an important parameter for fitting the data, and it should be estimated not fixed.

2. Data of this kind can be more insightfully plotted on a log scale (presented in the project later). Also, the linear analysis (additive decomposition, periodogram, ARMA) are better on a log scale. The team is correct to note that comparing likelihoods on log and natural scale requires care (i.e., a Jacobian transformation, see the Measles and Polio case studies in the notes).

3. A log-SARMA benchmark would be a more rigorous test of model specification than SARMA.

4. Influenza cases is either lab-confirmed cases (which depends critically on the amount of testing) or reported influenza-like illness (ILI) which is not all influenza. Later, it seems that what is called "cases" is ILI.

5. It is not clear what is learned from the additive decomposition that cannot be seen more clearly from other plots. To study seasonality of nonlinear and highly variable systems, a simple line plot of superposed seasonal trajectories can be more informative.

6. Listing the raw data is usually inappropriate. Similarly, showing raw R summaries is usually less helpful than identifying and explaining key properties. In other words, showing data and summary statistics follows the same rule as other figures and tables: if you present it, discuss it and explain what you learned from this representation.

7. The ARMA section might be too long. The main thing acquired from this section is a benchmark to compare against mechanistic model fits, so it is better to focus on the mechanistic models.

8. Sec 5.6 is not a poor man's profile as defined in the notes, it is a slice. The plot in 5.6.1 shows terrible likelihoods for large rho, much lower than the benchmark, but this is just due to a mismatch between the state parameters and the proposed reporting rate. This is fixed in Sec 5.7. It would be better to focus more on the profile than the slice.

9. The references are helpful. They do not conform to usual standards for scientific research, but focusing on links rather than full text references makes practical sense in the context of this final project.

10. The report is long and would be easier to read if it were more selective about what is included. Things that are tried and superseded can be noted in the main text and presented only in an appendix.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: covered (matched by finding: "poor man's profile lacks re-optimization — it is a conditional slice, not a profile likelihood")
- Human Issue #9: missed
- Human Issue #10: missed

**Findings classification:**
- Finding 1 (H reset conflict): A — Major; double-specification of H accumulation creates conflicting reset mechanism
- Finding 2 (data re-loaded without filter): A — Major; basic SEIRS section reads different CSV without year filter, breaking reproducibility
- Finding 3 (filter applied twice): A — Major; filter(YEAR < 2024) applied redundantly in advanced SEIRS section
- Finding 4 (likelihood comparison not valid): A — Major; SARMA vs POMP likelihood comparison ignores particle filter Monte Carlo variance and lacks formal test
- Finding 5 (gamma biologically implausible): A — Major; estimated gamma implies ~19-day immunity duration, far shorter than biological range
- Finding 6 (profile rho grid too narrow): A — Major; profile likelihood for rho evaluated over a very narrow grid that may not cover the true MLE
- Finding 7 (MIF2 hyperparameters not reported): A — Major; key global search settings and convergence diagnostics absent from main text
- Finding 8 (duplicate gamma in rw_sd_profile): A — Major; duplicate named argument silently overwrites first entry and may exclude phase from perturbation
- Finding 9 (COVID suppression date inconsistent): C — Moderate; covid_end = 333 comment in seirs_beta.R gives inconsistent date (2023 vs 2021)
- Finding 10 (R=0 initialization implausible): C — Moderate; initializing R=0 in January 2015 inflates susceptible pool for an established endemic disease
- Finding 11 (periodogram axis labels misleading): C — Moderate; spec.pgram returns cycles per week, but axis is labeled and abline placed as if cycles per year
- Finding 12 (antigenic drift model not validated): C — Moderate; Brownian motion sigma_mut parameterization not checked against known antigenic data
- Finding 13 (H accumulator includes imported cases): C — Moderate; imported cases added to H bypass E compartment, inconsistent with accumulator definition
- Finding 14 (non-standard AIC argument): C — Minor; "mathematical inconsistency" between ARMA(3,0) and ARMA(3,1) is unclear and non-standard language
- Finding 15 (poor man's profile mislabeled): D — Minor; poor man's profile described as profile likelihood but is actually a conditional slice without re-optimization (matches Human Issue #8)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 9 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: covered (matched by finding: "fixed parameters without sensitivity analysis — k listed among fixed parameters that should be examined")
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: covered (matched by finding: "rho profile evaluates range incompatible with global MLE"; also matched by finding: "alpha and gamma poor man's profiles are likelihood slices, not profile likelihoods")
- Human Issue #9: missed
- Human Issue #10: missed

**Findings classification:**
- Major Issue 1 (rho profile range incompatible with global MLE): B — rho poor man's profile grid [0.02, 0.08] excludes global MLE at rho ≈ 0.004; profile evaluated in wrong region (matches Human Issue #8)
- Major Issue 2 (alpha/gamma profiles are likelihood slices, not profiles): B — alpha and gamma poor man's profiles do not re-optimize nuisance parameters; explicitly a slice not a profile; same issue noted for rho poor man's profile (matches Human Issue #8)
- Major Issue 3 (H accumulator double-zeroing): A — H is zeroed both by accumvars mechanism and manually in Csnippet, discarding first sub-step's incidence (~14% systematic undercount)
- Major Issue 4 (data span misrepresented): A — text states 2015–2024 but code filters YEAR < 2024, excluding all 2024 data
- Major Issue 5 (COVID suppression amplitude A ≈ 0.088 biologically implausible): A — estimated 8.8% reduction in beta is inconsistent with observed near-zero cases during 2020–2022
- Major Issue 6 (R0 < 1 at baseline): A — interpretable final model implies R0 ≈ 0.962, inconsistent with literature range [1.19, 1.37]
- Major Issue 7 (no conditional log-likelihood plots or ESS monitoring): A — no per-observation loglik contributions or particle filter ESS reported
- Minor: auto-installing packages: C — second code chunk installs packages without user consent
- Minor: imported cases added to H: C — rpois-imported cases added to both I and H, inflating observation likelihood during COVID near-zero period
- Minor: fixed parameters without sensitivity analysis (k, sigma_mut, r1, r2, mu_EI, phase): D — k among several fixed parameters with no profile or sensitivity table; k specifically should be estimated (matches Human Issue #1)
- Minor: two competing best models not clearly resolved: C — highest-likelihood model vs interpretable fixed-rho model both presented as final without designating a primary result
- Minor: wide filter thresholds in global search pair plots: C — loglik > max - 2000 or -500 thresholds are too wide; standard is 10–20 log-units
- Minor: spectral periodogram harmonics not acknowledged: C — higher-harmonic peaks beyond frequency=1 not discussed
- Minor: biological plausibility appendix uses unlabeled model parameters: C — frho parameters used without clearly labeling which model version
- Minor: notation inconsistency (mu_RS): C — mu_RS and mu_{RS} used interchangeably in inline math and code
- Minor: ARMA "mathematical inconsistency" framing is wrong: C — AIC(3,1) > AIC(3,0) framed as "mathematical inconsistency" rather than optimization artifact

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "Invalid direct log-likelihood comparison between SARIMA and POMP models")
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: covered (matched by finding: "The 'poor man's profile' over alpha and gamma is a global-search scatter, not a true profile likelihood")
- Human Issue #9: missed
- Human Issue #10: missed

**Findings classification:**
- Major #1 (Invalid SARIMA-POMP log-likelihood comparison): B — flags the direct numerical comparison as invalid because SARIMA uses Gaussian and POMP uses negative-binomial observation models (matches Human Issue #2)
- Major #2 (Accumulator variable H manually reset in rprocess Csnippet, conflicts with accumvars): A — identifies a systematic off-by-one measurement error from dual reset mechanisms
- Major #3 (Poor man's profile for alpha and gamma is a global-search scatter, not a true profile likelihood): B — identifies that what is labeled a profile is not a genuine profile likelihood with re-optimization at each fixed parameter value (matches Human Issue #8)
- Major #4 (Profile for rho covers range that excludes the global MLE): A — the rho profile range [0.02, 0.04] does not include the global MLE of rho = 0.0042
- Major #5 (Implausible COVID suppression amplitude and hard-coded suppression parameters): A — A = 0.088 (9%) is inconsistent with near-zero cases; r1, r2 fixed without sensitivity analysis; two-year discrepancy in t_end
- Major #6 (No conditional log-likelihood or ESS diagnostics for the final model): A — no per-observation log-likelihood plots or ESS traces for the final BVGC-SEIRS model
- Major #7 (Over-parameterization leads to unidentifiable and biologically implausible estimates): A — 16-parameter model on one observable; gamma implies ~10-19 day immunity waning; tenfold rho discrepancy unresolved
- Minor (Typo in data loading — ILITOTA vs ILITOTAL): C — inline fallback arima call would silently fail if RDS is missing
- Minor (H accumulator semantics in basic SEIRS model): C — choice of dN_EI over dN_IR is reasonable but not explicitly justified
- Minor (Data double-filtering for complex SEIRS model): C — redundant filter call could cause silent data range mismatch on re-render
- Minor (Vaccine effectiveness interpolation is annual, not seasonal): C — flat within-season effectiveness not assessed for sensitivity
- Minor (Poor man's profile rho grid range 0.02–0.08 differs from true profile range 0.02–0.04): C — inconsistent ranges make the narrative comparison invalid
- Minor (No sessionInfo or package versions documented): C — pomp API changes across versions; reproducibility not assured
- Minor (Total computational cost not reported): C — CPU-hours, worker count, and walltime absent; cannot assess computational adequacy
- Minor (rho_grid has only 30 points and 5 IF2 runs, modest for 16-parameter model): C — resulting profile described as "considerably noisier," consistent with undercomputation
- Minor (ChatGPT used for scientific table and plot generation): C — AI-generated content used without independent verification
- Minor (Section title says SARMA errors but initial identification uses pure ARMA; non-standard SARMA notation): C — minor naming inconsistency that may confuse readers

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 10 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: covered (matched by finding: C5 — k fixed at 10 without profiling)
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: covered (matched by finding: C3 — likelihood slice CI is invalid)
- Human Issue #9: missed
- Human Issue #10: missed

**Findings classification:**
- C1: A — H accumulator likely zeroed before dmeas evaluation
- C2: A — profile likelihood for rho truncated at its lower boundary
- C4: A — gamma biologically implausible and identifiability-entangled with mu_RS
- C3: D — CI drawn from likelihood slice is invalid (matches Human Issue #8)
- C5: D — k fixed at 10 without profiling or random-walk standard deviation (matches Human Issue #1)
- C6: C — log-likelihood standard errors vary; evaluation protocol not documented
- X2: C — "posterior predictive check" terminology is incorrect
- X3: C — number of mif2 starting points for main model global searches not reported

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 3 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 8 | 5 | 5 | 3 |
| B (AI major, human also found) | 0 | 2 | 2 | 0 |
| C (AI minor, human missed) | 6 | 8 | 10 | 3 |
| D (AI minor, human also found) | 1 | 1 | 0 | 2 |
| E (Human found, AI missed) | 9 | 8 | 8 | 8 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 0 | 1 | 9 | 1/10 = 10% | 8 | 6 | 14/15 = 93% |
| Charlie | 2 | 1 | 8 | 2/10 = 20% | 5 | 8 | 13/16 = 81% |
| Doug | 2 | 0 | 8 | 2/10 = 20% | 5 | 10 | 15/17 = 88% |
| Evan | 0 | 2 | 8 | 2/10 = 20% | 3 | 3 | 6/8 = 75% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #3: A log-SARMA benchmark would be a more rigorous test of model specification than SARMA. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #4: Influenza cases is either lab-confirmed cases (which depends critically on the amount of testing) or reported influenza-like illness (ILI) which is not all influenza. Later, it seems that what is called "cases" is ILI. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #5: It is not clear what is learned from the additive decomposition that cannot be seen more clearly from other plots. To study seasonality of nonlinear and highly variable systems, a simple line plot of superposed seasonal trajectories can be more informative. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #6: Listing the raw data is usually inappropriate. Similarly, showing raw R summaries is usually less helpful than identifying and explaining key properties. In other words, showing data and summary statistics follows the same rule as other figures and tables: if you present it, discuss it and explain what you learned from this representation. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #7: The ARMA section might be too long. The main thing acquired from this section is a benchmark to compare against mechanistic model fits, so it is better to focus on the mechanistic models. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #9: The references are helpful. They do not conform to usual standards for scientific research, but focusing on links rather than full text references makes practical sense in the context of this final project. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #10: The report is long and would be easier to read if it were more selective about what is included. Things that are tried and superseded can be noted in the main text and presented only in an appendix. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 7 out of 10 human issues (70%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #2: Data of this kind can be more insightfully plotted on a log scale (presented in the project later). Also, the linear analysis (additive decomposition, periodogram, ARMA) are better on a log scale. The team is correct to note that comparing likelihoods on log and natural scale requires care (i.e., a Jacobian transformation, see the Measles and Polio case studies in the notes). (Covered only by Doug)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 1 |
| Evan | 0 |
