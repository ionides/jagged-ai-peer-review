# Ned-Clean Analysis — W22 Project 20

---

## Human Issues

1. For EDA and/or ARMA and/or wavelets, the log of the data might be worth examining since population dynamics are usually closer to linear on a log scale.
2. The noise on the maximization is quite large, making the crude 1.92 log-unit cutoff for the profile primarily noise; a smoothed likelihood estimate could improve this.
3. The use of Box-Cox transformations for ARMA models is not explained, and exactly what was done is unclear; it is also unclear whether ARMA likelihoods are properly adjusted for the transformation.
4. The SARMA model is fitted to a different time interval than the mechanistic model, so it no longer provides a benchmark likelihood.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "Degenerate Profile Likelihood Confidence Intervals — single-point CIs from noisy maximization")
- Human Issue #3: covered (matched by finding: "BoxCox Transformation Is Applied to Shifted Data With Arbitrary Constant — offset +1050 unjustified")
- Human Issue #4: covered (matched by finding: "Incomparable Likelihoods Between SARIMA and SIRS Models — different data subsets")

**Findings classification:**
- Major 1 (profile trace for b groups by a — copy-paste bug): A — critical coding bug in b-profile trace visualization
- Major 2 (degenerate profile CIs, single-point min=max): B — profile likelihood failure from noisy maximization (matches Human Issue #2)
- Major 3 (sin vs cos inconsistency in seasonality model): A — mathematical description contradicts code implementation
- Major 4 (null hypothesis test not executed): A — core scientific question left unanswered despite profiles being computed
- Major 5 (very poor final POMP likelihood, lack of convergence): A — IF2 non-convergence and poor log-likelihood
- Major 6 (local search uses %do% not %dopar%): A — parallelization inconsistency in local search
- Major 7 (incomparable SARIMA vs SIRS likelihoods — different subsets): B — invalid benchmark comparison across different data subsets (matches Human Issue #4)
- Major 8 (dmeasure returns lik=0 instead of -Inf): A — measurement model boundary condition coding error
- Major 9 (section 4.4 missing): A — unexplained gap in section numbering
- Minor 10 (BoxCox offset +1050 arbitrary and unjustified): D — unexplained Box-Cox transformation choice (matches Human Issue #3)
- Minor 11 (rho in partrans but in fixed_params — inconsistency): C — parameter specification inconsistency
- Minor 12 (BoxCox offset +1050 — duplicate concern): C — same as Minor 10; Human Issue #3 already claimed
- Minor 13 (SARIMA prediction description inaccurate): C — minor description inaccuracy in training window
- Minor 14 (no model diagnostics beyond visual simulation): C — missing conditional log-likelihood and ESS analysis
- Minor 15 (pandemic week 260 hardcoded): C — hardcoded threshold not documented in mathematical writeup

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 1 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "Profile likelihoods are degenerate: confidence intervals collapse to single points")
- Human Issue #3: covered (matched by finding: "BoxCox transformation introduces an arbitrary offset (+1050) with no justification")
- Human Issue #4: covered (matched by finding: "POMP log-likelihood is three orders of magnitude below SARIMA, no meaningful benchmark interpretation")

**Findings classification:**
- Major 1 (dmeasure returns 0 instead of log-likelihood -Inf): A — measurement model boundary coding error
- Major 2 (sin vs cos inconsistency): A — mathematical description contradicts code implementation
- Major 3 (POMP log-likelihood far below SARIMA, no meaningful benchmark): B — invalid benchmark comparison identifying different datasets (matches Human Issue #4)
- Major 4 (profile likelihoods degenerate, single-point CIs): B — profile CI failure from noisy/sparse optimization (matches Human Issue #2)
- Major 5 (rho fixed at implausible value): A — reporting rate fixed with inadequate justification
- Major 6 (local search uses %do% not %dopar%): A — parallelization inconsistency
- Major 7 (global search box from full likelihood table including implausible values): A — profile starting box anchored to biologically unreasonable parameter ranges
- Major 8 (missing convergence diagnostics for global search): A — no trace plots for global search
- Major 9 (SARIMA and POMP on different datasets, invalid comparison): A — additional framing of invalid benchmark (Human Issue #4 already claimed by Major 3)
- Minor: AIC table values normalized (per-observation), not standard scale: C — AIC normalization not clarified
- Minor: rho in partrans but in fixed_params inconsistency: C — parameter specification inconsistency
- Minor: BoxCox offset +1050 not justified: D — unexplained Box-Cox constant (matches Human Issue #3)
- Minor: SARIMA prediction description inaccurate: C — minor description inaccuracy in training window
- Minor: No model diagnostics (ESS, conditional log-likelihood): C — missing particle filter diagnostics
- Minor: Pandemic week 260 hardcoded: C — hardcoded threshold not documented

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 1 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "Insufficient Computational Effort — Np=1000, Nmif=50 insufficient, non-convergence not treated as requiring more computation")
- Human Issue #3: covered (matched by finding: "BoxCox transformation +1050 offset not justified")
- Human Issue #4: covered (matched by finding: "Invalid SARIMA-vs-POMP Log-Likelihood Comparison — dataset-length and observation-model mismatch")

**Findings classification:**
- Major 1 (global search anti-pattern: initialized from local IF2 result mf1): A — inherited cooled IF2 state prevents genuine global exploration
- Major 2 (profile base object mf1 inherits cooled state): A — profile optimization compromised by same anti-pattern
- Major 3 (invalid SARIMA vs POMP comparison — dataset length and observation model): B — invalid benchmark comparison (matches Human Issue #4)
- Major 4 (insufficient computational effort — non-convergence unaddressed): B — profile failure from inadequate optimization budget (matches Human Issue #2)
- Major 5 (no valid benchmark comparison): A — absence of any proper quantitative benchmark (Human Issue #4 already claimed by Major 3)
- Major 6 (rho fixed at misspecified value without justification): A — reporting rate fixed with inadequate derivation
- Major 7 (H accumulates recoveries not infections — accumulator semantics): A — measurement model accumulates wrong compartment transition
- Minor: local search %do% not %dopar%: C — parallelization inconsistency
- Minor: SARIMA prediction without quantitative error: C — no RMSE or CRPS for held-out interval
- Minor: sin vs cos inconsistency: C — mathematical description contradicts code
- Minor: BoxCox offset +1050 not justified: D — unexplained Box-Cox constant (matches Human Issue #3)
- Minor: rho justification arithmetic unclear: C — denominator confusion in rho derivation
- Minor: "Poor man's profile" includes all results from sirs_lik.csv: C — exploratory profile contaminated by local-search results
- Minor: CIs not reported explicitly in conclusion: C — a_ci and b_ci computed but not stated
- Minor: Informal reference (office hours): C — uncitable source used for scientific claim
- Minor: Code quality (commented-out blocks): C — analysis version unclear from Rmd
- Minor: Missing model diagnostics (ESS, conditional log-likelihood): C — no particle filter diagnostics shown

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 1 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "[22.20.1/2] Profile likelihood failure renders the central hypothesis untestable")
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "[22.20.3] Likelihood comparison across model classes requires care — different windows and transformations")

**Findings classification:**
- Major [22.20.1/2] (profile likelihood failure, degenerate CIs): B — profile CI failure from insufficient optimization (matches Human Issue #2)
- Major [22.20.4] (IF2 non-convergence — parameters trending upward after 50 iterations): A — non-convergence acknowledged but not addressed before profiles run
- Major [22.20.5] (cos vs sin inconsistency): A — mathematical description contradicts code
- Major [22.20.6] (b-profile trace copy-paste error — groups by a not b): A — incorrect visualization of b-profile trace
- Minor [22.20.3] (likelihood comparison invalid — different windows and transforms): D — invalid SARIMA vs SIRS benchmark comparison (matches Human Issue #4)
- Minor [22.20.7] (rho fixed without sensitivity analysis): C — reporting rate fixed with no sensitivity check
- Minor [22.20.8] (mu_IR = 7/week implies ~1-day recovery, biologically implausible): C — implausible parameter estimate not discussed
- Minor [22.20.M1] (dmeasure lik=0 incorrect for log scale): C — measurement model boundary condition coding error
- Minor: Np=1000 at run_level=3 is low: C — insufficient particle count for final results
- Minor: AIC table headers garbled: C — AIC table formatting issue

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 7 | 7 | 5 | 3 |
| B (AI major, human also found) | 2 | 2 | 2 | 1 |
| C (AI minor, human missed) | 5 | 5 | 9 | 5 |
| D (AI minor, human also found) | 1 | 1 | 1 | 1 |
| E (Human found, AI missed) | 1 | 1 | 1 | 2 |

---

## Per-Reviewer Metrics

**Alex**
- Human Recall = (B+D) / (B+D+E) = (2+1) / (2+1+1) = 3/4 = **75.0%**
- AI-Unique Rate = (A+C) / (A+B+C+D) = (7+5) / (7+2+5+1) = 12/15 = **80.0%**

**Charlie**
- Human Recall = (B+D) / (B+D+E) = (2+1) / (2+1+1) = 3/4 = **75.0%**
- AI-Unique Rate = (A+C) / (A+B+C+D) = (7+5) / (7+2+5+1) = 12/15 = **80.0%**

**Doug**
- Human Recall = (B+D) / (B+D+E) = (2+1) / (2+1+1) = 3/4 = **75.0%**
- AI-Unique Rate = (A+C) / (A+B+C+D) = (5+9) / (5+2+9+1) = 14/17 = **82.4%**

**Evan**
- Human Recall = (B+D) / (B+D+E) = (1+1) / (1+1+2) = 2/4 = **50.0%**
- AI-Unique Rate = (A+C) / (A+B+C+D) = (3+5) / (3+1+5+1) = 8/10 = **80.0%**

---

## Cross-Reviewer Aggregation

**Consensus misses:** Human issues that every reviewer failed to cover.

- Human Issue #1 (log transform for EDA/ARMA/wavelets): missed by Alex, Charlie, Doug, Evan — all four reviewers missed this.

Count: 1 out of 4 human issues (25%).

**Unique finds per reviewer:** Human issues covered by exactly one reviewer and missed by all others.

All three issues that were covered (Human Issues 2, 3, 4) were covered by all four reviewers. No human issue was uniquely found by only one reviewer.

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |

**Universal AI-only flags:** Issues raised by every reviewer that the human did not mention.

The following concerns were raised as Major findings by all four reviewers (Alex, Charlie, Doug, Evan) and were not covered by the human review:

- sin vs cos inconsistency between mathematical description and code (raised as Major by Alex, Charlie; as Major by Evan; as Minor by Doug — not universal as Major, but raised by all four)
- dmeasure returns lik=0 instead of -Inf for invalid states (raised as Major by Alex, Charlie; as Minor by Evan; not explicitly by Doug as a standalone — actually Doug does not have this as a standalone item)

Checking universality (raised by ALL four reviewers in any category):
- sin/cos inconsistency: Alex Major 3, Charlie Major 2, Doug Minor, Evan Major [22.20.5] — raised by all four. Human did not mention it.
- dmeasure lik=0 bug: Alex Major 8, Charlie Major 1, Evan Minor [22.20.M1] — raised by three of four (Doug does not raise this as a standalone item). Not universal.
- rho fixed with inadequate justification: Alex Minor 12, Charlie Major 5, Doug Major 6, Evan Minor [22.20.7] — raised by all four. Human did not mention it.
- Local search %do% not %dopar%: Alex Major 6, Charlie Major 6, Doug Minor, Evan (not raised explicitly as standalone) — three of four.
- Profile likelihoods degenerate: all four raised this, but Human Issue #2 partially covers it (it's a B/D match, not AI-only).

Universal AI-only flags (raised by all four reviewers, human did not mention):
1. sin vs cos inconsistency between mathematical model description and C code implementation
2. rho (reporting rate) fixed at an inadequately justified value

Count: 2 universal AI-only flags.
