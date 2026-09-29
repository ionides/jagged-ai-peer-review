# Comparator Analysis — W22 Project 02

---

## Human Issues

1. The profile for beta is flat over this interval. You have not justified a confidence interval of around 3-7.

2. Evidence of a strong nonlinear relationship between beta and eta.

3. The conclusion "the confidence intervals of the two transmission rates are sill the same" is wrong. The obtained intervals are determined only by the interval over which the profile has been calculated. It would be more correct to say that in both cases beta is unidentifiable over this interval.

4. The weak identifiability might suggest exploring the possibility of fixing one or more parameter at scientifically plausible values.

5. References at the end are not all cited when relevant during the main text. This makes it harder to see what is attributable to each reference.

6. At least some members in the group were aware of https://kingaa.github.io/sbied/ebola/ and the project would have been stronger had this connection been made explicit.

7. Figure captions, figure numbers and section numbers would make it easier for referees.

8. It would be good to have a benchmark likelihood, e.g. from log ARMA. The project references a previous project which does carry out a benchmark analysis, and one could follow their approach.

---

## Alex

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Profile Likelihood for Beta Spans the Entire Search Box, Indicating Non-Identifiability That Is Not Adequately Addressed")
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "Profile Likelihood for Beta Spans the Entire Search Box, Indicating Non-Identifiability That Is Not Adequately Addressed"; also matched by finding: "Conclusions Attribute Same CI to Both Countries Due to Same Search Box")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed

**Findings classification:**
- Finding 1 (Measurement Model Fundamentally Misspecified): A — H used directly in binomial, zero observations mishandled
- Finding 2 (Wrong Population Size for Sierra Leone): A — N=6190280 used instead of 16190280
- Finding 3 (Profile Likelihood for Beta Not Constructed Correctly): A — beta not truly fixed at grid values in profile search
- Finding 4 (Funeral Compartment F Modeled as Flow, Not Stock): A — F has no memory across time steps, inconsistent with Weitz-Dushoff
- Finding 5 (Death Rate Hardcoded at 50% with Deterministic Rounding): A — CFR fixed, conservation error from rounding
- Finding 6 (R0 Not Computed or Discussed): A — no R0 formula, estimates, or literature comparison
- Finding 7 (mu_EI Epidemiologically Implausible): A — rate implies sub-day incubation period
- Finding 8 (mu_IR Similarly Implausible): A — rate implies ~1 day infectious period
- Finding 9 (Search Box Inconsistent with Initial Simulation): C — Beta=17 in simulation vs. [3,7] in global search
- Finding 10 (F_size Fixed and Not Estimated): C — funeral size fixed at 50 without justification or sensitivity analysis
- Finding 11 (Profile Likelihood Spans Entire Search Box): D — CI [3.003, 6.974] nearly equals search box [3,7], non-identifiability not addressed (matches Human Issues #1 and #3)
- Finding 12 (bake() Called Twice for Same File): C — redundant cache call, poor code organization
- Finding 13 (No Convergence Diagnostics for Global Search): C — trace plots absent for global search, only pairs plots shown
- Finding 14 (EDA Is Superficial): C — single time-series per country, no ACF or deaths-cases analysis
- Finding 15 (Conclusions Attribute Same CI to Both Countries Due to Same Search Box): D — same CI is artifact of identical search bounds, main finding self-refuted (matches Human Issue #3)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Profile Likelihood for Beta is a Likelihood Slice, Not a Profile — CI spans entire search box, no inferential content")
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "Profile Likelihood for Beta is a Likelihood Slice, Not a Profile — CI artifact of search box"; also matched by finding: "Conclusion That Guinea and Sierra Leone Have 'Same Transmission Rate' is Unsupported")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: covered (matched by finding: "No Non-Mechanistic Benchmark Comparison")

**Findings classification:**
- Finding 1 (Measurement Model H Misspecification): A — severe misspecification of binomial dmeas/rmeas applied to accumulator H
- Finding 2 (Profile Likelihood is a Likelihood Slice): B — profile is a scatter plot over random Beta values, CI spans entire search box (matches Human Issues #1 and #3)
- Finding 3 (F_size in partrans): A — F_size is fixed yet included in log() parameter transformation without justification
- Finding 4 (No Benchmark Comparison): B — no ARMA or non-mechanistic benchmark likelihood reported (matches Human Issue #8)
- Finding 5 (Biologically Implausible Estimates): A — mu_EI ≈ 14.9 day^-1 implies ~96-minute incubation period, not flagged
- Finding 6 (No Overdispersion): A — binomial measurement model used without justification; negative binomial preferred
- Finding 7 (rw.sd Too Small): A — rw.sd = 0.002 is 10x smaller than course standard, limiting optimizer exploration
- Finding 8 (No Quantitative GoF in Text): A — log-likelihood values computed but never reported in paper body
- Finding 9 (Initial Conditions Implausible): A — I₀ fixed at 482 (Guinea) and 935 (Sierra Leone) without justification
- Finding 10 (Sierra Leone Population Misspecified): A — N ≈ 6.19 million used instead of actual 2014 value ~7.1 million
- Finding 11 (Conclusion of Same Transmission Rate Unsupported): B — identical CI bounds are artifact of search box design, not data inference (matches Human Issue #3)
- Finding 12 (Funeral Compartment F Assigned Not Accumulated): A — F set equal to instantaneous new funerals per step rather than accumulated
- Finding 13 (No Model Diagnostics): A — no conditional log-likelihood plots, ESS traces, or residual checks
- Finding 14 (Global Search Results Duplicated): A — bind_rows(results, results) bug inflates apparent search size
- Finding 15 (No R0 Discussion): A — no reproduction number computed despite motivating SEIRDF model by R0 concerns

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 12 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 0 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Profile Likelihood Is Flat Across Entire Box; Confidence Interval Is Uninformative")
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "Profile Likelihood Is Flat Across Entire Box; Confidence Interval Is Uninformative"; also matched by finding: "Conclusions Overstate Comparison Between Countries")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: covered (matched by finding: "No Benchmark Comparison Against Non-Mechanistic Model")

**Findings classification:**
- Finding 1 (Global Search Anchored to Local mif2 Result Object): A — global IF2 replicates inherit a near-cooled schedule from mifs_local[[1]], so the search does not genuinely explore the parameter box
- Finding 2 (Measurement Model: Binomial Without Overdispersion): A — dmeas/rmeas use binomial rather than negative binomial, misspecifying overdispersion
- Finding 3 (Accumulator Variable H Accumulates Wrong Flow): A — H += dN_IR (exits from I) rather than dN_EI (entries into I), creating a semantic mismatch with reported cases
- Finding 4 (No Benchmark Comparison Against Non-Mechanistic Model): B — no ARMA/ARIMA baseline log-likelihood comparison presented (matches Human Issue #8)
- Finding 5 (Population N for Sierra Leone Contains a Factor-of-10 Error): A — code uses N=6190280 instead of N=16190280, inflating effective contact rate ~2.6×
- Finding 6 (Profile Likelihood Is Flat Across Entire Box; Confidence Interval Is Uninformative): B — profile spans nearly the entire search box; concluding "similar transmission rates" is invalid (matches Human Issues #1 and #3)
- Finding 7 (F_size Fixed Without Justification): A — F_size fixed at 50 with no citation or sensitivity analysis; only the product Beta2/F_size is identifiable
- Finding 8 (rw.sd Values Are Very Small Relative to Parameter Scales): A — rw.sd=0.002 not calibrated; no convergence diagnostics presented
- Finding 9 (dmeas/rmeas Boundary Handling Inconsistency): C — tol used instead of exact dbinom(0,H,rho) for zero-count days
- Finding 10 (rm(list=ls()) Inside Document): C — workspace cleared mid-document, breaking reproducibility
- Finding 11 (No Quantitative Goodness-of-Fit Values Reported): C — maximum log-likelihood values never stated for either country
- Finding 12 (No Model Diagnostics Beyond Simulation Plots and Pairs Plots): C — no ESS traces, conditional log-likelihoods, or filtering-distribution simulations
- Finding 13 (Conclusions Overstate Comparison Between Countries): D — "very similar transmission rates" conclusion drawn from two flat CIs spanning the same search box, which is not a valid inference (matches Human Issue #3)
- Finding 14 (Missing pomp and Package Version Information): C — no sessionInfo() or renv lockfile
- Finding 15 (Initial Conditions Are Fixed Without Sensitivity Analysis): C — hardcoded initial I values and R=(1-eta)*N initialization not justified

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: covered (matched by finding: "22.02.1 — flat profile for beta, CI [3,7] not a valid confidence interval")
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "22.02.1 — flat profile for beta, CI [3,7] not a valid confidence interval"; also matched by finding: "22.02.M4 — equal CIs conclusion is a circular artifact of shared search bounds")
- Human Issue #4: covered (matched by finding: "22.02.7 — parameter convergence absent; suggests fixing parameters from literature")
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "22.02.M6 — all figures lack captions")
- Human Issue #8: covered (matched by finding: "22.02.6 — no benchmark comparison with non-mechanistic models")

**Findings classification:**
- 22.02.1: B — flat profile for beta; CI [3,7] not a valid confidence interval; central scientific claim unsupported (matches Human Issues #1 and #3)
- 22.02.2: A — profile likelihood methodology nonstandard; nuisance parameters not optimized at each fixed beta
- 22.02.3: A — no replicated pfilter evaluation; all likelihood values come from biased mif2 internal output
- 22.02.4: A — measurement model distribution never specified; observation equation form absent
- 22.02.5: A — funeral exposure term likely violates conservation of susceptibles
- 22.02.6: B — no benchmark comparison with non-mechanistic models (matches Human Issue #8)
- 22.02.7: B — parameter convergence absent for most parameters; suggests fixing parameters from literature (matches Human Issue #4)
- 22.02.M1: C — mu_EI values biologically implausible (imply ~1–2 hour incubation period)
- 22.02.M2: C — population N for Sierra Leone inconsistent between text and trace plot
- 22.02.M3: C — death rate fixed at 50% without citation or justification
- 22.02.M4: D — equal CIs conclusion is a circular artifact of shared search bounds (matches Human Issue #3)
- 22.02.M5: C — Np and Nmif not reported in text
- 22.02.M6: D — all figures lack captions (matches Human Issue #7)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 8 | 12 | 6 | 4 |
| B (AI major, human also found) | 0 | 3 | 2 | 3 |
| C (AI minor, human missed) | 5 | 0 | 6 | 4 |
| D (AI minor, human also found) | 2 | 0 | 1 | 2 |
| E (Human found, AI missed) | 6 | 5 | 5 | 3 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 0 | 2 | 6 | 2/8 = 25% | 8 | 5 | 13/15 = 87% |
| Charlie | 3 | 0 | 5 | 3/8 = 38% | 12 | 0 | 12/15 = 80% |
| Doug | 2 | 1 | 5 | 3/8 = 38% | 6 | 6 | 12/15 = 80% |
| Evan | 3 | 2 | 3 | 5/8 = 62% | 4 | 4 | 8/13 = 62% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #2: Evidence of a strong nonlinear relationship between beta and eta. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #5: References at the end are not all cited when relevant during the main text. This makes it harder to see what is attributable to each reference. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #6: At least some members in the group were aware of https://kingaa.github.io/sbied/ebola/ and the project would have been stronger had this connection been made explicit. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 3 out of 8 human issues (38%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #4: The weak identifiability might suggest exploring the possibility of fixing one or more parameter at scientifically plausible values. (Covered only by Evan)
- Human Issue #7: Figure captions, figure numbers and section numbers would make it easier for referees. (Covered only by Evan)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 2 |
