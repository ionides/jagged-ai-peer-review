# Ned-Clean Analysis — W22 Project 16

---

## Human Issues

1. The rationale for choosing Moscow (Russia) is unclear; Russian data was notoriously problematic, with reporting likely influenced by political considerations.
2. The model has no measurement or process over-dispersion, which might cause problems fitting to data and could explain convergence difficulties.
3. A benchmark (e.g., ARMA or iid negative binomial) would help see whether the mechanistic model has reasonable statistical fit.
4. The model has a static (time-invariant) structure, whereas COVID-19 transmission is a dynamic process influenced by changing policies and variants; a time-varying component would be more appropriate.
5. The data characteristics (small early peak, long plateau, no decreasing trend at the end) demonstrate the time-invariant model cannot depict the data well, as verified by local and global search results.
6. Many parameters are fixed, which could be problematic if one or more are accidentally fixed in a way that disagrees with the data.
7. Math punctuation is erratic; periods should appear at the end of the last line of math, not on a blank line.
8. The arrow from A to Sy is surprising and could be considered for deletion; asymptomatics by definition do not lead to symptoms.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "No benchmark comparison or likelihood benchmarks")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed

**Findings classification:**
- Major 1 (SIR-CDR model completely unexecuted): A — SIR-CDR code all set to eval=FALSE, no results produced
- Major 2 (Sy updated twice with conflicting logic, SIR-CDR): A — double-counting flows in Sy compartment
- Major 3 (dN_SyH subtracted twice in else branch, SIR-CDR): A — systematic under-counting in Sy
- Major 4 (Force-of-infection: dual binomial draws from same compartment S): A — inflated transmission from sequential draws
- Major 5 (Measurement model: D used directly as mu in dnbinom, doubly stochastic): A — non-standard measurement structure, zero-sensitivity when D=0
- Major 6 (Global search underpowered: 20 restarts, 1000 particles): A — inadequate exploration of 4-dimensional parameter space
- Major 7 (Profile likelihood over wrong range [0.01, 0.95]): A — profile excludes observed optimum, no inferential value
- Major 8 (No model comparison or likelihood benchmarks): B — matches Human Issue #3
- Major 9 (eta stated as 0.002 in text but coded as 0.0002): A — presentation error indicating insufficient proofreading
- Minor 10 (Mu_SyR renamed from Mu_R between models without explanation): C — self-contradictory text
- Minor 11 (Equation 169 repeats dN_SyH with two definitions): C — LaTeX transcription error introduces ambiguity
- Minor 12 (Capacity constraint C bug zeros Sy whenever overflow): C — C scoping bug producing incorrect dynamics
- Minor 13 (Population mismatch: data has 12,692,466 vs model's 11,920,000): C — biased per-capita rate estimates
- Minor 14 (No ESS diagnostic plots for any particle filter run): C — missing standard validation diagnostic
- Minor 15 (Conclusion overstates value of unexecuted SIR-CDR model): C — no empirical basis for the claim

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "No comparison to any non-mechanistic benchmark")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "Fixed parameters not justified with sensitivity analysis")
- Human Issue #7: missed
- Human Issue #8: missed

**Findings classification:**
- Major 1 (SIR-CDR model never fitted — primary claim unsubstantiated): A — all SIR-CDR code at eval=FALSE
- Major 2 (Sy updated twice with conflicting logic, SIR-CDR): A — double-counting flows in Sy compartment
- Major 3 (dN_SyH label appears twice in equations, notation error): A — written model does not match code, reproducibility failure
- Major 4 (Profile likelihood is a slice not a profile — confidence intervals invalid): A — profile never reaches MLE, 387 log-unit gap
- Major 5 (No comparison to non-mechanistic benchmark): B — matches Human Issue #3
- Major 6 (No convergence diagnostics for iterated filtering): A — convergence failure not investigated, bimodal global search distribution
- Major 7 (Fixed parameters not justified with sensitivity analysis): B — matches Human Issue #6
- Major 8 (SIR-D clamping code: Sy zeroed before proportional allocation, silent bug): A — R and D underestimated in overflow case
- Major 9 (eta stated as 0.002 in text but coded as 0.0002): A — presentation discrepancy indicating proofreading failure
- Minor (dmeas sums log-likelihoods additively — valid but unconventional, potential underflow): C — numerical concern in non-log mode
- Minor (D_rate biologically conflated with competing hazard, death rate tied to Mu_SyR): C — parametrization breaks when Mu_SyR is large
- Minor (Profile threshold uses incorrect reference loglik — profile never reaches global MLE): C — displayed threshold has no interpretive value
- Minor (run_level=2: only 4 replicates and 10 points for profile): C — profile informationally void even if range were correct
- Minor (No simulation-based diagnostics for SIR-D): C — no conditional log-likelihood, no filtering ESS analysis
- Minor ("miss-specified" consistently misspelled throughout): C — persistent typographical error
- Minor (No sessionInfo() or package version documentation): C — reproducibility concern across R versions

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "No non-mechanistic benchmark comparison")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "Fixed parameters not estimated or given profile likelihoods")
- Human Issue #7: missed
- Human Issue #8: missed

**Findings classification:**
- Major 1 (SIR-CDR accumulator: rho*dN_SyR double-counted in both C and Rr; text-code discrepancy for C): A — same individual counted as confirmed and recovered simultaneously
- Major 2 (dN_SyH defined twice in equations with different rates): A — notation error obscures model structure
- Major 3 (Capacity mechanism zeros Sy whenever overflow — conservation violation): A — sets Sy to zero whenever Sy+H > Cap
- Major 4 (Global IF2 initialized from previous mif2 result, inheriting near-zero cooling): A — global replicates anchored near local optimum
- Major 5 (Profile over range excluding MLE by two orders of magnitude): A — no valid confidence interval can be extracted
- Major 6 (No non-mechanistic benchmark comparison): B — matches Human Issue #3
- Major 7 (No goodness-of-fit metric reported for SIR-CDR model): A — no log-likelihood, no simulation, no visual diagnostics
- Major 8 (Self-diagnosed convergence failure paired with substantive parameter interpretation): A — conclusions derived from acknowledged non-converged results
- Major 9 (SIR-D: Sy zeroed before proportional allocation, analogous bug in A-compartment): A — R and D systematically underestimated in overflow cases
- Minor (Mu_SyR absent from paramnames but referenced in text): C — text-code mismatch about identifiability structure
- Minor (partrans declared twice — in pomp() and in mif2()): C — risk of inconsistency if one copy updated
- Minor (Fixed parameters not estimated or given profile likelihoods): D — matches Human Issue #6
- Minor (run_level=2 uses only 1000 particles — very low for 5-state model): C — substantial Monte Carlo error in likelihood comparisons
- Minor (Simulation envelope not shown): C — only 5 trajectories, no quantile envelope
- Minor (Conclusion misstates paper's primary contribution): C — framing should reflect exploratory failure modes

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "SIR-CDR uses Poisson — underdispersed")
- Human Issue #3: covered (matched by finding: "No benchmark comparison")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed

**Findings classification:**
- 22.16.A (Process model error: death hazard coupled to Mu_SyR multiplicatively in dN_SyD): A — optimizer inflates Mu_SyR to increase death probability, causing implausible estimates
- 22.16.B (Profile likelihood range [0,1] excludes MLE near 100+): A — entire profile outside likelihood ridge, uninformative
- 22.16.C (No benchmark comparison): B — matches Human Issue #3
- 22.16.D (SIR-CDR measurement model uses Poisson — underdispersed for city-scale COVID data): B — matches Human Issue #2
- 22.16.E (Sequential binomial draws from shared compartment — conservation violation): A — clipping is not equivalent to proper Euler-Multinomial step
- 22.16.F (Cap parameter unspecified — not in parameter list or optimization results): C — unclear if fixed, estimated, or ignored
- 22.16.G (k not perturbed in local search — overdispersion parameter not optimized): C — whether intentional should be clarified
- 22.16.H (Spread in converged global search runs suggests flat likelihood or Monte Carlo noise): C — identifiability concern reinforced
- 22.16.I (dN_SyH appears twice in SIR-CDR equations): C — typographical error on p. 6
- 22.16.J (ESS trace not shown for SIR-D model): C — cannot distinguish computational inadequacy from model misspecification

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 8 | 7 | 8 | 3 |
| B (AI major, human also found) | 1 | 2 | 1 | 2 |
| C (AI minor, human missed) | 6 | 7 | 5 | 5 |
| D (AI minor, human also found) | 0 | 0 | 1 | 0 |
| E (Human found, AI missed) | 7 | 6 | 6 | 6 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

**Alex:**
- Human Recall = (B+D) / (B+D+E) = (1+0) / (1+0+7) = 1/8 = 12.5%
- AI-Unique Rate = (A+C) / (A+B+C+D) = (8+6) / (8+1+6+0) = 14/15 = 93.3%

**Charlie:**
- Human Recall = (B+D) / (B+D+E) = (2+0) / (2+0+6) = 2/8 = 25.0%
- AI-Unique Rate = (A+C) / (A+B+C+D) = (7+7) / (7+2+7+0) = 14/16 = 87.5%

**Doug:**
- Human Recall = (B+D) / (B+D+E) = (1+1) / (1+1+6) = 2/8 = 25.0%
- AI-Unique Rate = (A+C) / (A+B+C+D) = (8+5) / (8+1+5+1) = 13/15 = 86.7%

**Evan:**
- Human Recall = (B+D) / (B+D+E) = (2+0) / (2+0+6) = 2/8 = 25.0%
- AI-Unique Rate = (A+C) / (A+B+C+D) = (3+5) / (3+2+5+0) = 8/10 = 80.0%

---

## Cross-Reviewer Aggregation

**Consensus misses:** Human issues that every reviewer failed to cover.

- Human Issue #1: Moscow/Russian data quality — missed by all 4 reviewers (4 out of 4)
- Human Issue #4: Static time-invariant model inappropriate for COVID — missed by all 4 reviewers (4 out of 4)
- Human Issue #5: Data characteristics demonstrate time-invariant model fails — missed by all 4 reviewers (4 out of 4)
- Human Issue #7: Math punctuation erratic — missed by all 4 reviewers (4 out of 4)
- Human Issue #8: Arrow from A to Sy should be reconsidered — missed by all 4 reviewers (4 out of 4)

Total consensus misses: 5 out of 8 human issues (62.5%)

**Unique finds per reviewer:** Human issues covered by exactly one reviewer and missed by all others.

- Human Issue #2 (no over-dispersion): covered only by Evan (22.16.D — Poisson underdispersed); Alex, Charlie, Doug missed it.
- Human Issue #6 (fixed parameters problematic): covered by Charlie (Major 7) and Doug (minor bullet); missed by Alex and Evan. This is not a unique find for either since two reviewers cover it.

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 1 |

Human Issue #3 (no benchmark) was covered by all four reviewers — not a unique find.
Human Issue #6 (fixed parameters) was covered by Charlie and Doug — not unique to either.
Human Issue #2 (no over-dispersion) was covered only by Evan.

**Universal AI-only flags:** Issues raised by every reviewer that the human did not mention.

Checking which AI-unique findings appear across all four reviewers:

- Profile likelihood over wrong range / slice not profile: raised by Alex (Major 7), Charlie (Major 4), Doug (Major 5), Evan (22.16.B) — all 4 reviewers, human missed. Count: 1
- dN_SyH appears twice in SIR-CDR equations: raised by Alex (Minor 11), Charlie (Major 3), Doug (Major 2), Evan (22.16.I) — all 4 reviewers, human missed. Count: 1
- SIR-D clamping/overflow code bug (Sy zeroed before allocation): raised by Alex (implicitly via Major 2-3 focus on SIR-CDR), Charlie (Major 8), Doug (Major 9), Evan (22.16.A covers related parametrization; 22.16.E covers conservation). Alex's review does not explicitly describe this SIR-D-specific bug (Alex's Major 2-3 are SIR-CDR bugs). So not universal — Alex misses this specific SIR-D bug.

Checking more carefully:
- SIR-CDR never executed: raised by Alex (Major 1), Charlie (Major 1), Doug (Major 7 — "no goodness-of-fit metric reported for SIR-CDR"), Evan does not explicitly flag this as a standalone issue (Evan discusses poor fit but not the eval=FALSE finding). Not universal.

Only two clear universal AI-only flags:
1. Profile likelihood range excludes the MLE / profile is a likelihood slice with no inferential value (Alex Major 7, Charlie Major 4, Doug Major 5, Evan 22.16.B)
2. dN_SyH label appears twice in SIR-CDR process model equations (Alex Minor 11, Charlie Major 3, Doug Major 2, Evan 22.16.I)

Universal AI-only flags count: 2
