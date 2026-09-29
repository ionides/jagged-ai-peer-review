# Comparator Analysis — W22 Project 10

---

## Human Issues

1. Analyzing weekly total might be superior to a weekly moving average. The latter induces dependence between observations.

2. The authors did a good job of getting the SEAPIRD model to work. Perhaps SIR could have done much better if initial conditions (especially, I) were estimated rather than fixed. There is a big mismatch with the data for the first 20 timepoints.

3. The paper used a Negative Binomial measurement model for the SIR model and a normal approximation to the Binomial for the SEAPIRD model. This difference, and its potential consequences, should be discussed.

4. Figure captions and numbers would be appreciated by the readers.

5. The omicron SIR model is fitted with $N=5\times 10^5$ whereas in the text and elsewhere the authors report $N=5\times 10^7$. This is a major problem, only detectable via careful reading by someone with access to the code. It could be avoided by not hard-coding numbers in the report.

6. The introduction could have been documented with more supporting references.

7. The authors apparently did not use caching (e.g., bake and stew) for their results. This may have made it harder to develop the code. It also makes it harder for those who re-run the code during review.

8. The SEAPIRD model comes from https://ionides.github.io/531w21/final_project/project13/blinded.html. The authors do not give credit to this (which is their reference [5]) and instead acknowledge incorrectly [6]. Hopefully this is a typo. However, the relationship to [5] could have been better explained beyond this favorable interpretation.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "SEAPIRD measurement model statistically incorrect — Normal approximation with wrong parameterization")
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "Inconsistent population size between SIR and SEAPIRD models — SIR uses N=50M, SEAPIRD uses N=500K"; also matched by finding: "SIR global search passes N=500,000 while model stated to use N=50,000,000")
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed

**Findings classification:**
- Finding 1 (Inconsistent population size SIR vs SEAPIRD): B — inconsistent N across models, SIR uses 50M while SEAPIRD uses 500K (matches Human Issue #5)
- Finding 2 (No profile likelihood or formal confidence intervals): A — no uncertainty quantification for any estimated parameter
- Finding 3 (SEAPIRD measurement model statistically incorrect — Normal approximation): B — normal approximation with wrong parameterization for SEAPIRD observation model (matches Human Issue #3)
- Finding 4 (SIR global search passes N=500,000 vs stated N=50,000,000): B — hardcoded N=500,000 in global search contradicts stated model specification (matches Human Issue #5)
- Finding 5 (No likelihood benchmark against null/ARMA on common scale): A — likelihood comparison across models is invalid without common observation scale
- Finding 6 (SEAPIRD branching of exposed class statistically invalid): A — rounding of binomial draw fractions violates conservation of individuals
- Finding 7 (mif2 particle count too low — Np=100 for SIR local search): A — Np=100 causes severe particle degeneracy
- Finding 8 (Intervention covariate structure arbitrary): A — 50-day windows not tied to any known policy or epidemiological events
- Finding 9 (SIR rinit sets H=169 instead of 0): C — accumulator variable incorrectly initialized to 169 at t0
- Finding 10 (SEAPIRD rinit sets S=N, population not conserved): C — S=N while I=169 at initialization violates population accounting
- Finding 11 (Weekly periodicity identified but not incorporated into POMP models): C — day-of-week covariate absent from both SIR and SEAPIRD models
- Finding 12 (Smoothed vs raw data inconsistency between models): C — SEAPIRD text claims smoothed data but code uses raw, inconsistent with SIR
- Finding 13 (SEAPIRD global best-fit parameters biologically implausible): C — mu_AR=3.49/day implies <7-hour asymptomatic recovery
- Finding 14 (No convergence diagnostics for SIR — eval=FALSE): C — SIR log likelihood convergence plots suppressed in rendered document
- Finding 15 (Data preprocessing slice operation fragile): C — non-intuitive trimming logic unexplained, November data inclusion unjustified

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "SEAPIRD measurement model uses Normal distribution without adequate justification; the change between SIR and SEAPIRD measurement models makes log-likelihood comparisons non-interpretable")
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "Inconsistent population size N in the SIR global search — N=500000 in global search vs N=50000000 in model and local search")
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed

**Findings classification:**
- Finding 1 (H initialized to 169): A — accumulator variable H initialized to 169 instead of 0 in SIR rinit (Major, no human match)
- Finding 2 (Inconsistent N in SIR global search): B — global search hard-codes N=500000 while model uses N=50000000 (matches Human Issue #5)
- Finding 3 (SEAPIRD rmeasure/dmeasure inconsistent): A — rmeasure and dmeasure use different transformations of the measurement variable within SEAPIRD (Major, no human match)
- Finding 4 (No profile likelihoods): A — no profile likelihoods or confidence intervals for any parameter (Major, no human match)
- Finding 5 (SIR convergence diagnostics suppressed): A — SIR diagnostic chunk marked eval=FALSE and never rendered (Major, no human match)
- Finding 6 (No non-mechanistic benchmark comparison): A — ARMA log-likelihood never numerically contrasted against POMP log-likelihoods (Major, no human match)
- Finding 7 (SEAPIRD Normal measurement model unjustified): B — Normal distribution used for SEAPIRD without justification; difference from SIR NegBin makes log-likelihood comparisons non-interpretable (matches Human Issue #3)
- Finding 8 (Small rw.sd values): A — rw.sd values of 0.005 likely insufficient for SIR parameters (Major, no human match)
- Finding 9 (Np=100 particles): C — SIR local search uses only Np=100 particles, a debugging-level setting (Minor, no human match)
- Finding 10 (Global search not sorted): C — SEAPIRD global search best result selected by row position rather than by log-likelihood (Minor, no human match)
- Finding 11 (SEAPIRD S=N initialization): C — SEAPIRD sets S=N while also setting I=169, violating population conservation (Minor, no human match)
- Finding 12 (dN_EA/dN_EP non-integer split): C — nearbyint rounding on E-to-P and E-to-A transitions can violate population conservation (Minor, no human match)
- Finding 13 (Spectrum frequency interpretation): C — frequency units and relationship between peak_freq and omega_1 are unclear (Minor, no human match)
- Finding 14 (Arbitrary 50-day cutoffs): C — intervention breakpoints at 50 and 100 days not tied to documented policy events (Minor, no human match)
- Finding 15 (No biological plausibility discussion): C — extreme parameter estimates (mu_ID near zero, alpha=0.0285) presented without comparison to literature (Minor, no human match)

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
- Human Issue #3: covered (matched by finding: "Normal measurement model is poorly motivated and inconsistent with NegBin used in SIR")
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "Population size inconsistency between SIR local and global searches — N=500,000 vs N=50,000,000")
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed

**Findings classification:**
- Major #1 (SEAPIRD rmeasure adds D to cases while dmeasure subtracts deaths — internal inconsistency): A — code-level mismatch between dmeasure and rmeasure in SEAPIRD
- Major #2 (Normal measurement model poorly motivated for count data, inconsistent with NegBin in SIR): B — matches Human Issue #3
- Major #3 (No profile likelihoods computed for any parameter): A — parameter identifiability unassessed
- Major #4 (N=500,000 in SIR global search vs N=50,000,000 in local search and text): B — matches Human Issue #5
- Major #5 (Invalid direct log-likelihood comparison between ARMA and POMP models): A — different observation distributions make comparison invalid
- Major #6 (Insufficient computational effort — 16 replicates, Np=100 for SIR local): A — non-convergence misattributed to biology
- Major #7 (No valid benchmark comparison for mechanistic models): A — no same-scale non-mechanistic baseline
- Major #8 (SIR accumulator H tracks recoveries dN_IR, not new infections dN_SI): A — semantic mismatch between accumulator and observed data
- Minor: week-7 periodicity not incorporated in POMP observation model: C — unmodeled periodicity degrades particle filter
- Minor: SEAPIRD initial conditions set S=N ignoring initially infected, violating population conservation: C — S + I > N at time zero
- Minor: H initialized to 169 in sir_rinit despite H being an accumvar reset each step: C — initial value unexplained
- Minor: global SIR results not sorted before selecting row 1 as best: C — best parameters may not actually be best
- Minor: log-likelihood convergence diagnostic chunk marked eval=FALSE and not rendered: C — essential diagnostics excluded
- Minor: no comparison of parameter estimates to scientific literature values: C — biological plausibility unchecked
- Minor: pairs plots include non-finite log-likelihoods without filtering: C — axes distorted by -Inf values

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
- Human Issue #3: covered (matched by finding: "Normal measurement model in SEAPIRD inappropriate; contrasts with NB used in SIR")
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "SEAPIRD N=500,000 vs SIR N=50,000,000 unexplained discrepancy")
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed

**Findings classification:**
- 22.10.1: A — ARMA model selection internally inconsistent (ARMA(4,4) has lower AIC but ARMA(3,3) selected)
- 22.10.2: A — MA roots nearly on unit circle indicating near non-invertibility
- 22.10.3: A — SEAPIRD fit on 7-day smoothed data while SIR/ARMA fit on raw data, invalidating central comparison
- 22.10.4: B — Normal measurement model in SEAPIRD inappropriate for count data; SIR correctly used negative binomial (matches Human Issue #3)
- 22.10.5: A — SIR local search MC standard error of 6.98 log-likelihood units is too large to support reliable comparison
- 22.10.6: A — SEAPIRD parameters severely non-identifiable; large discrepancies between local and global optima unexplored
- 22.10.8: A — No profile likelihoods or confidence intervals computed for any parameter
- 22.10.9: D — SEAPIRD population size N=500,000 vs SIR N=50,000,000; 100-fold difference unexplained (matches Human Issue #5)
- 22.10.10: C — Np and Nmif not reported in text
- 22.10.11: C — 7-day periodicity identified in spectral analysis but not incorporated into POMP models
- 22.10.12: C — ARMA residual diagnostics show heavy tails and autocorrelation; distributional mismatch not diagnosed

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
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 5 | 6 | 6 | 6 |
| B (AI major, human also found) | 3 | 2 | 2 | 1 |
| C (AI minor, human missed) | 7 | 7 | 7 | 3 |
| D (AI minor, human also found) | 0 | 0 | 0 | 1 |
| E (Human found, AI missed) | 6 | 6 | 6 | 6 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 3 | 0 | 6 | 2/8 = 25% | 5 | 7 | 12/15 = 80% |
| Charlie | 2 | 0 | 6 | 2/8 = 25% | 6 | 7 | 13/15 = 87% |
| Doug | 2 | 0 | 6 | 2/8 = 25% | 6 | 7 | 13/15 = 87% |
| Evan | 1 | 1 | 6 | 2/8 = 25% | 6 | 3 | 9/11 = 82% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #1: Analyzing weekly total might be superior to a weekly moving average. The latter induces dependence between observations. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #2: The authors did a good job of getting the SEAPIRD model to work. Perhaps SIR could have done much better if initial conditions (especially, I) were estimated rather than fixed. There is a big mismatch with the data for the first 20 timepoints. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #4: Figure captions and numbers would be appreciated by the readers. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #6: The introduction could have been documented with more supporting references. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #7: The authors apparently did not use caching (e.g., bake and stew) for their results. This may have made it harder to develop the code. It also makes it harder for those who re-run the code during review. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #8: The SEAPIRD model comes from https://ionides.github.io/531w21/final_project/project13/blinded.html. The authors do not give credit to this (which is their reference [5]) and instead acknowledge incorrectly [6]. Hopefully this is a typo. However, the relationship to [5] could have been better explained beyond this favorable interpretation. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 6 out of 8 human issues (75%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

(none)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |
