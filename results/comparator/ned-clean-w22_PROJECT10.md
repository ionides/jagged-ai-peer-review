# Ned-Clean Analysis — W22 Project 10

---

## Human Issues

1. Analyzing weekly total might be superior to a weekly moving average — the moving average induces dependence between observations.
2. SIR could have done much better if initial conditions (especially I) were estimated rather than fixed; there is a big mismatch with the data for the first 20 timepoints.
3. The paper used a Negative Binomial measurement model for the SIR model and a normal approximation for the SEAPIRD model; this difference and its potential consequences should be discussed.
4. Figure captions and numbers would be appreciated by the readers.
5. The Omicron SIR model is fitted with N=5x10^5 whereas in the text and elsewhere N=5x10^7 is reported — a major problem only detectable via careful reading; could be avoided by not hard-coding numbers.
6. The introduction could have been documented with more supporting references.
7. The authors apparently did not use caching (e.g., bake and stew) for their results, making development and review harder.
8. The SEAPIRD model comes from a prior project (reference [5]) but credit is given incorrectly to [6]; the relationship to [5] could have been better explained.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "SEAPIRD measurement model — Normal approximation with wrong parameterization")
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "SIR global search passes N=500,000 while model states N=50,000,000")
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed

**Findings classification:**
- Major 1 (N inconsistency between SIR and SEAPIRD models): A — broad population-size inconsistency between the two model families (N=500K vs N=50M)
- Major 2 (No profile likelihood or formal CIs): A — missing uncertainty quantification for all parameters
- Major 3 (SEAPIRD Normal approximation with wrong parameterization): B — matches Human Issue #3
- Major 4 (SIR global search hardcodes N=500,000): B — matches Human Issue #5
- Major 5 (No valid likelihood benchmark against ARMA on common scale): A — invalid cross-family log-likelihood comparison
- Major 6 (SEAPIRD branching rounding error violates conservation): A — exposed-class split produces non-integer compartment sizes
- Major 7 (Np=100 too low for SIR local search): A — particle count far too small for reliable inference
- Major 8 (Intervention covariate structure arbitrary): A — 50-day windows not tied to epidemiological events
- Minor 9 (SIR rinit sets H=169 instead of 0): C — accumulator initialized incorrectly
- Minor 10 (SEAPIRD S=N without removing initially infected): C — population conservation violated at t0
- Minor 11 (Weekly periodicity not incorporated into POMP models): C — spectrum identifies 7-day cycle but neither model accounts for it
- Minor 12 (Smoothed data for SEAPIRD vs raw for SIR — inconsistent comparison): C — data preprocessing inconsistency across models
- Minor 13 (SEAPIRD global best-fit parameters biologically implausible): C — extreme parameter values suggest poor identifiability
- Minor 14 (SIR convergence diagnostics suppressed — eval=FALSE): C — log-likelihood trace plots not rendered
- Minor 15 (Data preprocessing slice operation fragile and unexplained): C — logic not explained and may trim valid data

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "SEAPIRD measurement model Normal distribution without adequate justification")
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "Inconsistent population size N in the SIR global search")
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed

**Findings classification:**
- Major 1 (H=169 in SIR rinit — implementation bug): A — accumulator variable incorrectly initialized
- Major 2 (Inconsistent N in SIR global search): B — matches Human Issue #5
- Major 3 (SEAPIRD rmeasure and dmeasure inconsistent): A — generative and evaluative measurement models differ
- Major 4 (No profile likelihoods or CIs): A — missing uncertainty quantification
- Major 5 (SIR convergence diagnostics suppressed — eval=FALSE): A — log-likelihood trace plots not rendered
- Major 6 (No non-mechanistic benchmark comparison): A — ARMA vs POMP comparison not explicitly quantified
- Major 7 (SEAPIRD Normal measurement model without adequate justification): B — matches Human Issue #3
- Major 8 (rw.sd values likely insufficient): A — perturbation magnitudes too small for adequate exploration
- Minor 9 (SIR local search uses only Np=100 particles): C — too few particles for reliable inference
- Minor 10 (Global search best result selected without sorting by log-likelihood): C — first row taken instead of highest-loglik row
- Minor 11 (SEAPIRD initializes S=N without removing initially infected): C — population conservation violated at t0
- Minor 12 (SEAPIRD dN_EA/dN_EP split can produce non-integer compartment sizes): C — rounding error in exposed-class branching
- Minor 13 (Spectrum analysis frequency interpretation not precise): C — unit labels and relationship between peaks unclear
- Minor 14 (SEAPIRD intervention structure arbitrary 50-day cutoffs): C — cutoffs not tied to documented policy events
- Minor 15 (No discussion of parameter estimates' biological plausibility): C — extreme values not compared to epidemiological literature

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
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
- Human Issue #3: covered (matched by finding: "Normal measurement model poorly motivated and inappropriate for count data")
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "Population size inconsistency between SIR local and global searches")
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed

**Findings classification:**
- Major 1 (SEAPIRD rmeasure adds deaths, mismatch with dmeasure): A — generative and evaluative measurement models are inconsistent
- Major 2 (Normal measurement model poorly motivated): B — matches Human Issue #3
- Major 3 (No profile likelihoods): A — missing parameter identifiability assessment
- Major 4 (Population size inconsistency SIR local vs global — N=500K vs N=50M): B — matches Human Issue #5
- Major 5 (Invalid direct log-likelihood comparison ARMA vs POMP): A — different distributional families make comparison invalid
- Major 6 (Insufficient computational effort — Np=100, 16 replicates): A — particle count and replicate count too low
- Major 7 (No benchmark comparison for mechanistic models): A — no common-scale non-mechanistic baseline
- Major 8 (H accumulator tracks recoveries not new infections — semantic mismatch): A — accumulator semantics misalign with observed data meaning
- Minor (Week-7 periodicity not incorporated in POMP models): C — spectrum identifies 7-day cycle but neither model accounts for it
- Minor (SEAPIRD initial S=N without removing infected): C — population conservation violated at t0
- Minor (H initialized to 169 in SIR rinit): C — accumulator incorrectly initialized
- Minor (Global SIR search uses [1,] without sorting by log-likelihood): C — best parameters not guaranteed to be highest-loglik
- Minor (Log-likelihood convergence diagnostic eval=FALSE): C — SIR convergence plots not rendered
- Minor (No discussion of parameter estimates relative to scientific literature): C — no comparison with published Omicron epidemiological estimates
- Minor (Pairs plots use unfiltered results including non-finite log-likelihoods): C — -Inf values distort axes

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "Normal measurement model inappropriate for count data")
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "SEAPIRD N=500,000 vs SIR N=50,000,000 — not explained")
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed

**Findings classification:**
- Major 22.10.3 (SEAPIRD fit on 7-day smoothed data invalidates central comparison): A — data inconsistency across models makes log-likelihood comparison invalid
- Major 22.10.4 (Normal measurement model inappropriate for count data): B — matches Human Issue #3
- Major 22.10.1 (ARMA model selection internally inconsistent — ARMA(4,4) lower AIC but ARMA(3,3) selected): A — model selection contradicts stated AIC criterion
- Major 22.10.2 (MA roots nearly on unit circle — near non-invertibility): A — boundary of invertibility, suggests model misspecification
- Major 22.10.6 (SEAPIRD parameters severely non-identifiable; between-search discrepancies not addressed): A — large parameter discrepancies across searches indicate flat or multimodal likelihood
- Major 22.10.8 (No profile likelihoods or CIs): A — missing uncertainty quantification for all parameters
- Major 22.10.5 (SIR local search MC standard error of 6.98 too large): A — computational imprecision renders local search result uninformative
- Minor 22.10.9 (SEAPIRD N=500,000 vs SIR N=50,000,000 — unexplained): D — matches Human Issue #5
- Minor 22.10.10 (Np and Nmif not reported in text): C — key computational settings omitted
- Minor 22.10.11 (7-day periodicity not incorporated into POMP models): C — spectrum identifies 7-day cycle but neither model accounts for it
- Minor 22.10.12 (ARMA residual diagnostics suggest distributional mismatch not analyzed): C — heavy tails in QQ plot not diagnosed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 3 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 6 | 6 | 6 | 6 |
| B (AI major, human also found) | 2 | 2 | 2 | 1 |
| C (AI minor, human missed) | 7 | 7 | 7 | 3 |
| D (AI minor, human also found) | 0 | 0 | 0 | 1 |
| E (Human found, AI missed) | 6 | 6 | 6 | 6 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

**Alex**
- Human Recall = (B+D) / (B+D+E) = (2+0) / (2+0+6) = 2/8 = **25.0%**
- AI-Unique Rate = (A+C) / (A+B+C+D) = (6+7) / (6+2+7+0) = 13/15 = **86.7%**

**Charlie**
- Human Recall = (B+D) / (B+D+E) = (2+0) / (2+0+6) = 2/8 = **25.0%**
- AI-Unique Rate = (A+C) / (A+B+C+D) = (6+7) / (6+2+7+0) = 13/15 = **86.7%**

**Doug**
- Human Recall = (B+D) / (B+D+E) = (2+0) / (2+0+6) = 2/8 = **25.0%**
- AI-Unique Rate = (A+C) / (A+B+C+D) = (6+7) / (6+2+7+0) = 13/15 = **86.7%**

**Evan**
- Human Recall = (B+D) / (B+D+E) = (1+1) / (1+1+6) = 2/8 = **25.0%**
- AI-Unique Rate = (A+C) / (A+B+C+D) = (6+3) / (6+1+3+1) = 9/11 = **81.8%**

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer (Alex, Charlie, Doug, Evan) failed to cover:

- Human Issue #1: Analyzing weekly total might be superior to a weekly moving average — the moving average induces dependence between observations.
- Human Issue #2: SIR could have done much better if initial conditions (especially I) were estimated rather than fixed; big mismatch with data for first 20 timepoints.
- Human Issue #4: Figure captions and numbers would be appreciated by the readers.
- Human Issue #6: The introduction could have been documented with more supporting references.
- Human Issue #7: The authors apparently did not use caching (e.g., bake and stew) for their results.
- Human Issue #8: The SEAPIRD model comes from a prior project (reference [5]) but credit is given incorrectly to [6].

**Count: 6 out of 8 human issues (75.0%)**

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Alex: none
- Charlie: none
- Doug: none
- Evan: none

(Human Issues #3 and #5 were each covered by all four reviewers, so no reviewer has a unique find.)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |

### Universal AI-only flags

Issues raised as Major by every reviewer that the human did not mention:

- No profile likelihoods or confidence intervals for any estimated parameter (raised as Major by Alex, Charlie, Doug, Evan)
- Normal measurement model for SEAPIRD is inappropriate/inadequately justified (raised as Major by all four — note: human Issue #3 is adjacent but asks for *discussion* of the difference, not specifically critique of the Normal choice; the AI reviewers go further in calling it an error)

Note on #3 and #5: these were matched to human issues, so they are not purely AI-only. The one truly universal AI-only Major is the profile likelihood omission.

Universal AI-only Major flags (not matched to any human issue, raised as Major by all four):
- No profile likelihoods or confidence intervals: raised as Major by Alex (Major 2), Charlie (Major 4), Doug (Major 3), Evan (Major 22.10.8). **Count: 1**
