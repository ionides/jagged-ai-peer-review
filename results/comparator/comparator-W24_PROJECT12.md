# Comparator Analysis — W24 Project 12

---

## Human Issues

1. Vaccination is an important phenomenon for COVID-19 transmission in this time interval. It is given some consideration in the discussion, but does not seem to be accounted for in the model. Waning immunity is addressed, but the model only permits transmission to R via infection, not vaccination.

2. Consider the following analysis: "From the plot of the residuals over time, the residuals are centered around zero. The variance also appears to be constant throughout the plot." The residuals being centered around zero is a mathematical necessity, and says nothing about the model fit. The variance may show some heteroskedasticity, but not extreme.

3. A well-executed project. It only has small novelty relative to previous class projects, but combining a bit of novelty with careful technique meets the requirements of a strong course project.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: contradiction (AI review lists six major methodological failures and concludes "methodological and implementation issues that limit confidence in the results"; human says "well-executed project" that "meets the requirements of a strong course project")

**Findings classification:**
- Finding 1 (global_results overwritten with 6 rows): A — permanent truncation of global search before profile likelihood construction
- Finding 2 (sigmaSE exceeds upper bound, at boundary): A — overdispersion parameter likely not well characterized; boundary issue unacknowledged
- Finding 3 (profile likelihood uses 11 coarse points, degenerate CI): A — upper CI bound hits the natural boundary of rho3, yielding uninterpretable interval
- Finding 4 (SEIRS fails to outperform ARMA by 32.5 log units): A — more complex model performs substantially worse with no systematic investigation
- Finding 5 (near-zero mu_RS, waning rate biologically meaningless): A — SEIRS extension provides essentially no waning immunity, not formally tested
- Finding 6 (eta = 0.89 implies implausible initial conditions): A — ~89% of population in Recovered at pandemic onset is epidemiologically implausible
- Finding 7 (H accumulates recoveries dN_IR, not infections): C — observation model uses recoveries instead of new cases, introducing a systematic lag
- Finding 8 (wave==2 floating-point comparison in C snippet): C — covariate interpolation can yield non-integer values, making exact equality unreliable
- Finding 9 (Delta and Omicron lumped into single b3): C — distinct transmission characteristics of two variants forced into one parameter
- Finding 10 (global search convergence diagnostics show widespread failure): C — particle filter collapse at multiple time points, variable Monte Carlo standard errors
- Finding 11 (only one profile likelihood computed): C — 12 other free parameters, including mu_RS and b3, receive no profile analysis
- Finding 12 (incorrect beta boundary interpretation): C — text description of global search box does not match box actually used for profile design
- Finding 13 (AIC table anomaly not diagnosed): C — optimizer warning suppressed and not mentioned; convergence issue unexplained
- Finding 14 (periodogram interpretation misleading): C — frequency-0 peak reflects trend/long memory, not absence of seasonality
- Finding 15 (W state variable serves no functional role): C — tracked throughout simulation but unused in measurement model or diagnostics
- Finding 16 (overall assessment contradicts human positive verdict): F — human reviewer calls this "a well-executed project" that "meets the requirements of a strong course project"; AI review concludes the project has "methodological and implementation issues that limit confidence in the results"

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 1 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: contradiction (AI says Major Revision with three structural gaps preventing key claims; human says well-executed project meeting requirements of a strong course project)

**Findings classification:**
- Major Issue 1 (SEIRS underperforms ARMA by 32.5 log units; gap misstated as small): A — no matching human issue
- Major Issue 2 (No nested SEIR vs. SEIRS comparison despite µ_RS ≈ 0): A — no matching human issue
- Major Issue 3 (Profile target ρ₃ perturbed during mif2, violating course standard): A — no matching human issue
- Major Issue 4 (Profile likelihood too sparse, 11 points instead of 30): A — no matching human issue
- Major Issue 5 (Only one of 13 parameters profiled; key identifiability unassessed): A — no matching human issue
- Major Issue 6 (Local search convergence: most runs plateau ~86 units below best result): A — no matching human issue
- Major Issue 7 (No convergence traces shown for global search): A — no matching human issue
- Minor Issue (Nsim=500 set but never used; simulation figures use nsim=5): C — no matching human issue
- Minor Issue (Measurement model described as truncated but implemented as censored): C — no matching human issue
- Minor Issue (Different breakpoints for β(t) and ρ(t) not discussed or justified): C — no matching human issue
- Minor Issue (ρ₃ > ρ₂ contradicts stated hypothesis, no explanation given): C — no matching human issue
- Minor Issue (No sessionInfo or package-version documentation): C — no matching human issue
- Minor Issue (AIC-table optimizer failures not resolved via multiple starting points): C — no matching human issue
- Minor Issue (Initial ι guess of 10 vs. MLE of ~200, no comment): C — no matching human issue
- Minor Issue (No sensitivity analysis for fixed parameters N or I(1)=1): C — no matching human issue
- Overall recommendation (Major Revision): F — contradicts Human Issue #3 (human says strong course project; AI says Major Revision citing three structural gaps)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 1 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed

**Findings classification:**
- Finding 1 (Global search initialized from previous mif2 result): A — global IF2 replicates inherit a decayed cooling schedule from a prior mif2d_pomp object, invalidating the global search claim
- Finding 2 (Profile likelihood for rho3 invalid): A — rho3 receives non-zero random-walk perturbations during the profile mif2 run, so the profile curve and derived CI are statistically invalid
- Finding 3 (Particle filter failures under-diagnosed): A — frequent near-zero ESS and conditional log-likelihood spikes are attributed to data artifacts without any model revision
- Finding 4 (Implausible mu_RS estimate): A — mu_RS implies a ~32-year immunity period; authors note it is "close to 0" but do not treat it as a misspecification signal
- Finding 5 (Insufficient model diagnostics): A — no per-time-point conditional log-likelihood decomposition, no filtering-distribution vs. forward-simulation comparison, no latent-state trajectory inspection
- Finding 6 (Profile CI uses profile maximum not global maximum): A — cutoff computed from profile max (-1404.86) rather than global MLE (-1403.97), making the CI anticonservative
- Finding 7 (Weak parameter identifiability not acted upon): A — broad ridges in pairs plots for most parameters acknowledged but no parameters fixed, no additional profiles computed, no model simplification
- Finding 8 (ARMA(2,2) equation duplicate subscript): C — second MA coefficient written as psi_1 instead of psi_2; typo, does not affect numerical results
- Finding 9 (Duplicate N column in profile artifact): C — two N columns in lev3_rho3_profile.rds due to redundant inclusion of N in both guesses and fixed_params
- Finding 10 (Force of infection drops alpha exponent): C — alpha=1 special case used in Csnippet without noting that alpha does not appear in paramnames, potentially confusing readers
- Finding 11 (SEIRS fails to beat ARMA benchmark, inadequately discussed): C — 32.5-unit log-likelihood gap dismissed as pandemic modeling difficulty without discussing measurement model differences or implications
- Finding 12 (No SEIR vs. SEIRS model comparison): C — near-zero mu_RS warrants a formal likelihood ratio test comparing nested SEIR model, which is absent
- Finding 13 (Reporting rate interval breakpoints inconsistent with transmission rate breakpoints): C — reporting rate changes at week 125 but transmission rate changes at week 72; mismatch not biologically motivated
- Finding 14 (Initial conditions fixed, no sensitivity analysis): C — E(0)=0 and I(0)=1 are biological minimums potentially inconsistent with February 2020 epidemic state; no sensitivity assessment
- Finding 15 (No sessionInfo or package version documentation): C — no sessionInfo() call or renv lockfile; reproducibility at risk given pomp API changes across versions

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed

**Findings classification:**
- Major 1: A — profile likelihood too sparse to support the reported confidence interval
- Major 2: A — non-convergence is pervasive but described as "not a problematic result"
- Minor 1: C — variable H undefined in the measurement model
- Minor 2: C — log-likelihood evaluation procedure not stated explicitly
- Minor 3: C — ESS collapse and conditional log-likelihood spikes attributed generically to holiday reporting
- Minor 4: C — mu_RS near zero framed as model inadequacy rather than identifiability constraint
- Minor 5: C — initial compartment allocations not stated
- Minor 6: C — AIC statement slightly misframes the relationship
- Minor 7: C — importation parameter iota described as population flow rather than infectious pressure term

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 2 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 6 | 7 | 7 | 2 |
| B (AI major, human also found) | 0 | 0 | 0 | 0 |
| C (AI minor, human missed) | 9 | 8 | 8 | 7 |
| D (AI minor, human also found) | 0 | 0 | 0 | 0 |
| E (Human found, AI missed) | 2 | 2 | 3 | 3 |
| F (Human-AI contradiction) | 1 | 1 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 0 | 0 | 2 | 0/2 = 0% | 6 | 9 | 15/15 = 100% |
| Charlie | 0 | 0 | 2 | 0/2 = 0% | 7 | 8 | 15/15 = 100% |
| Doug | 0 | 0 | 3 | 0/3 = 0% | 7 | 8 | 15/15 = 100% |
| Evan | 0 | 0 | 3 | 0/3 = 0% | 2 | 7 | 9/9 = 100% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #1: Vaccination is an important phenomenon for COVID-19 transmission in this time interval. It is given some consideration in the discussion, but does not seem to be accounted for in the model. Waning immunity is addressed, but the model only permits transmission to R via infection, not vaccination. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #2: Consider the following analysis: "From the plot of the residuals over time, the residuals are centered around zero. The variance also appears to be constant throughout the plot." The residuals being centered around zero is a mathematical necessity, and says nothing about the model fit. The variance may show some heteroskedasticity, but not extreme. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 2 out of 3 human issues (67%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

(none)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |
