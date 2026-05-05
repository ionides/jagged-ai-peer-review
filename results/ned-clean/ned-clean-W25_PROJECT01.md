# Ned-Clean Analysis — W25 Project 01

---

## Human Issues

1. k could be an important parameter and should be estimated, not fixed.
2. Data should be plotted on a log scale; the linear analyses (additive decomposition, periodogram, ARMA) are better on a log scale.
3. A log-SARMA benchmark would be a more rigorous test of model specification than SARMA.
4. It is not clear what the data represents — "influenza cases" may be lab-confirmed cases or ILI; the data type should be clarified upfront.
5. It is not clear what is learned from the additive decomposition; a simple line plot of superposed seasonal trajectories can be more informative.
6. Listing raw data and showing raw R summaries is usually inappropriate; presented data and summaries should be discussed and explained.
7. The ARMA section is too long; its main value is a benchmark, so mechanistic models should receive more focus.
8. Sec 5.6 is a likelihood slice, not a poor man's profile; it would be better to focus more on the proper profile.
9. References do not conform to usual standards for scientific research.
10. The report is long and would be more readable if more selective; superseded material should go to an appendix.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "likelihood comparison between SARMA and POMP not fully valid")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: covered (matched by finding: "poor man's profile lacks re-optimization, is technically a conditional likelihood slice")
- Human Issue #9: missed
- Human Issue #10: missed

**Findings classification:**
- Finding 1 (double-specification of H accumulation, conflicting reset): A — redundant H reset creates non-deterministic behavior
- Finding 2 (basic SEIRS loads different data file): A — data inconsistency breaks reproducibility and likelihood comparability
- Finding 3 (filter applied twice): A — double-filtering causes silent data truncation risk
- Finding 4 (SARMA vs POMP likelihood comparison invalid): B — matches Human Issue #3
- Finding 5 (gamma biologically implausible): A — gamma=6.95 implies ~19-day immunity; model acknowledges but does not resolve
- Finding 6 (rho profile over very narrow grid): A — profile grid too narrow to cover true MLE
- Finding 7 (MIF2 hyperparameters not reported): A — Nmif, Np, rw.sd not described; convergence not established
- Finding 8 (duplicate gamma entry in rw_sd_profile): A — duplicate named argument may silently restrict perturbation
- Finding 9 (COVID suppression end date inconsistent) [Moderate]: C — t_end=333 documented inconsistently across files
- Finding 10 (R=0 initialization biologically inconsistent) [Moderate]: C — starting all individuals as susceptible in January 2015 is implausible
- Finding 11 (periodogram labels misleading) [Moderate]: C — frequency axis label may be cycles/week not cycles/year
- Finding 12 (antigenic drift Brownian motion not validated) [Moderate]: C — sigma_mut fixed without checking against known antigenic data
- Finding 13 (H accumulator decremented by imported cases) [Moderate]: C — imported cases added to H inconsistently bypass E compartment
- Finding 14 (AIC selection argument non-standard) [Minor]: C — "mathematical inconsistency" language imprecise
- Finding 15 (poor man's profile lacks re-optimization) [Minor]: D — matches Human Issue #8

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "invalid direct log-likelihood comparison between SARIMA and POMP models")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: covered (matched by finding: "poor man's profile is global-search scatter, not a true profile likelihood")
- Human Issue #9: missed
- Human Issue #10: missed

**Findings classification:**
- Major #1 (invalid direct log-likelihood comparison SARIMA vs POMP): B — matches Human Issue #3
- Major #2 (H accumulator double reset): A — manual Csnippet reset conflicts with accumvars mechanism
- Major #3 (poor man's profile not true profile): B — matches Human Issue #8
- Major #4 (profile likelihood for rho excludes global MLE): A — rho profile range [0.02, 0.04] does not include MLE at 0.004
- Major #5 (COVID suppression amplitude implausible, parameters hard-coded): A — A=9% reduction insufficient for near-zero pandemic flu; r1, r2 fixed without sensitivity
- Major #6 (no conditional log-likelihood or ESS diagnostics): A — no per-observation log-likelihood plot or ESS traces for final model
- Major #7 (over-parameterization leads to unidentifiable estimates): A — 16 parameters on single observable; gamma and rho entangled
- Minor #9 (duplicate gamma in rw_sd): C — duplicate named argument may silently restrict perturbation
- Minor #10 (ILITOTA typo): C — column name typo in inline arima call
- Minor #11 (no seed/computational budget): C — intermediate global search RDS files lack documentation of Nmif, Np, nseq
- Minor #12 (profile range does not bracket MLE): C — rho CI cannot be valid since grid excludes true MLE
- Minor #13 (eta non-identifiability not addressed): C — eta uncertainty not propagated to other estimates via sensitivity analysis
- Minor #14 (posterior predictive check conflates forward simulation): C — simulations from MLE are not from filtering distribution
- Minor #15 (ChatGPT used for scientific table and code): C — AI-generated parameter interpretation table not independently verified

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "invalid direct log-likelihood comparison between SARIMA and POMP models")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: covered (matched by finding: "poor man's profile is global-search scatter, not a true profile likelihood")
- Human Issue #9: missed
- Human Issue #10: missed

**Findings classification:**
- Major #1 (invalid direct log-likelihood comparison): B — matches Human Issue #3
- Major #2 (H accumulator manually reset in rprocess): A — Csnippet reset conflicts with accumvars; off-by-one measurement error
- Major #3 (poor man's profile is global-search scatter): B — matches Human Issue #8
- Major #4 (profile likelihood for rho covers range excluding global MLE): A — profile [0.02, 0.04] excludes global MLE at rho=0.0042
- Major #5 (COVID suppression amplitude implausible, hard-coded parameters): A — A=9% too small; t_end inconsistently documented; r1/r2 fixed without sensitivity
- Major #6 (no ESS diagnostics for final model): A — no per-observation log-likelihood or ESS traces presented
- Major #7 (over-parameterization): A — gamma, rho entangled; nested LRT not conducted
- Minor: ILITOTA typo: C — column name typo in inline arima call
- Minor: H accumulator semantics in basic SEIRS: C — dN_EI vs dN_IR choice not fully justified; accumvars correct here
- Minor: Data double-filtering: C — filter applied twice; silent truncation risk on re-render
- Minor: Vaccine effectiveness interpolation annual not seasonal: C — constant-within-season assumption not assessed for sensitivity
- Minor: Poor man's profile rho grid range differs from true profile: C — ranges [0.02, 0.08] vs [0.02, 0.04] inconsistent for comparison
- Minor: No sessionInfo/package versions: C — pomp API changes; reproducibility uncertain
- Minor: Total computational cost not reported: C — CPU-hours, workers, walltime not stated
- Minor: rho grid insufficient computation per point: C — 5 IF2 runs per point with 150 total starts is modest for 16-parameter model
- Minor: ChatGPT for scientific table: C — AI-generated parameter table not independently verified
- Minor: SARMA notation non-standard: C — SARIMA(2,0,1)(0,0,2)[52] with regression component notation may cause confusion

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
- Human Issue #1: covered (matched by finding: "k fixed at 10 without profiling")
- Human Issue #2: missed
- Human Issue #3: contradiction (Evan says the SARMA vs POMP comparison is "appropriate and correctly executed" and "directly comparable"; human says log-SARMA would be more rigorous)
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: covered (matched by finding: "poor man's profile CI from likelihood slice is invalid")
- Human Issue #9: missed
- Human Issue #10: missed

**Findings classification:**
- C1 (H accumulator zeroed before dmeas evaluation) [Major]: A — manual Csnippet reset fires before measurement model, corrupting H
- C2 (profile likelihood for rho truncated at lower boundary) [Major]: A — peak at rho=0.02 is at grid edge; true MLE may lie below
- C4 (gamma biologically implausible, identifiability-entangled) [Major]: A — gamma=6.95 implies ~19-day immunity; flat likelihood above gamma=5
- C3 (poor man's profile CI from likelihood slice invalid) [Minor]: D — matches Human Issue #8
- C5 (k fixed at 10 without profiling) [Minor]: D — matches Human Issue #1
- C6 (log-likelihood SE varies; evaluation protocol not documented) [Minor]: C — number of pfilter replicates for final LL not stated
- X2 (posterior predictive check terminology incorrect) [Minor]: C — forward simulations at MLE mislabeled as posterior predictive
- X3 (number of mif2 starting points not reported for main model) [Minor]: C — nseq not stated for complete SEIRS searches
- S1/Summary: F — explicitly endorses SARMA vs POMP comparison as valid; contradicts Human Issue #3

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 3 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 1 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 7 | 5 | 5 | 3 |
| B (AI major, human also found) | 1 | 2 | 2 | 0 |
| C (AI minor, human missed) | 5 | 7 | 10 | 3 |
| D (AI minor, human also found) | 1 | 0 | 0 | 2 |
| E (Human found, AI missed) | 8 | 8 | 8 | 7 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 1 |

---

## Per-Reviewer Metrics

| Reviewer | B | D | E | F | Human Recall (B+D)/(B+D+E) | A | C | AI-Unique Rate (A+C)/(A+B+C+D) |
|----------|--:|--:|--:|--:|---------------------------:|--:|--:|-------------------------------:|
| Alex | 1 | 1 | 8 | 0 | 2/10 = 20.0% | 7 | 5 | 12/14 = 85.7% |
| Charlie | 2 | 0 | 8 | 0 | 2/10 = 20.0% | 5 | 7 | 14/16 = 87.5% |
| Doug | 2 | 0 | 8 | 0 | 2/10 = 20.0% | 5 | 10 | 15/17 = 88.2% |
| Evan | 0 | 2 | 7 | 1 | 2/9 = 22.2% | 3 | 3 | 6/8 = 75.0% |

Note: Evan's recall denominator is 9 (not 10) because Human Issue #3 is classified F (contradiction) and excluded from the recall denominator.

---

## Cross-Reviewer Aggregation

### Consensus Misses

Human issues that every reviewer failed to cover (E or F for all four):

| # | Human Issue | Alex | Charlie | Doug | Evan |
|---|-------------|------|---------|------|------|
| 2 | Data should be plotted on a log scale; linear analyses better on log scale | E | E | E | E |
| 4 | "Influenza cases" may be lab-confirmed or ILI; data type should be clarified upfront | E | E | E | E |
| 5 | It is not clear what is learned from the additive decomposition | E | E | E | E |
| 6 | Listing raw data and raw R summaries is inappropriate without discussion | E | E | E | E |
| 7 | The ARMA section is too long; should focus more on mechanistic models | E | E | E | E |
| 9 | References do not conform to usual standards for scientific research | E | E | E | E |
| 10 | The report is too long; superseded material should go to an appendix | E | E | E | E |

**7 out of 10 human issues were missed by every reviewer.**

### Unique Finds Per Reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #1 (k should be estimated, not fixed): covered only by Evan (D); missed by Alex, Charlie, Doug.

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 1 |

### Universal AI-Only Flags

Issues raised by every AI reviewer that the human did not mention (A in all four):

1. **H accumulator double-reset / manual reset conflict with accumvars**: The Csnippet manually resets H at integer time steps, conflicting with the pomp accumvars mechanism, potentially corrupting the measurement model. Raised by all four reviewers as Major.

2. **Profile likelihood for rho inadequate**: The rho profile covers a range [0.02, 0.04] that excludes the global MLE (rho ~ 0.004), making the reported CI invalid. Raised by all four reviewers as Major.

3. **Biologically implausible gamma and identifiability failure**: gamma = 6.95 implies ~19-day immunity duration; the data cannot identify gamma above a threshold; the issue is acknowledged but unresolved in the final model. Raised by all four reviewers as Major.

**3 universal AI-only flags (all classified Major by every reviewer).**
