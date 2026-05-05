# Ned-Clean Analysis — W24 Project 12

---

## Human Issues

1. Vaccination is not accounted for in the model — the model only permits transmission to R via infection, not vaccination, despite vaccination being an important phenomenon for COVID-19 transmission in this time interval.
2. The residual analysis incorrectly claims "residuals centered around zero" as meaningful evidence of model fit, when this is a mathematical necessity. The variance shows some heteroskedasticity but not extreme — the interpretation is misleading.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed

**Findings classification:**
- MAJOR 1 (global_results overwritten with top 6 rows before profile): A — global search results truncated before profile box construction
- MAJOR 2 (sigmaSE exceeds global search upper bound): A — overdispersion parameter at boundary; search region too restrictive
- MAJOR 3 (profile uses only 11 coarse grid points, degenerate CI): A — too few profile points, upper CI bound hits parameter boundary at 1.0
- MAJOR 4 (SEIRS fails to outperform ARMA by 32.5 log units): A — mechanistic model substantially worse than benchmark
- MAJOR 5 (near-zero mu_RS renders SEIRS extension biologically meaningless): A — waning immunity rate implies ~32-year immunity period
- MAJOR 6 (biologically questionable initial conditions, eta=0.89): A — ~72,000 people modeled as recovered before COVID spread in US
- MODERATE 7 (H accumulates recoveries not new infections): C — systematic lag introduced between epidemic curve and fitted observations
- MODERATE 8 (wave==2 floating-point comparison fragile): C — covariate linear interpolation causes inexact equality at sub-integer time steps
- MODERATE 9 (Delta and Omicron lumped into single b3): C — single transmission rate covers two substantially different variants
- MODERATE 10 (global search convergence diagnostics reveal widespread failure): C — ESS collapse and particle filter failures not quantified
- MODERATE 11 (only one profile likelihood computed): C — profiles absent for key parameters b1, b2, b3, mu_RS, eta
- MINOR 12 (incorrect Beta boundary interpretation): C — global search box and profile box inconsistent due to head(6) issue
- MINOR 13 (AIC table anomaly not fully explained): C — convergence warning suppressed and not mentioned
- MINOR 14 (periodogram interpretation misleading): C — frequency 0 dominance reflects trend, not absence of seasonality
- MINOR 15 (W state variable serves no functional role): C — running accumulator tracked but never used in measurement or diagnostics

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed

**Findings classification:**
- Major 1 (global search box for sigmaSE severely misspecified): A — search seeded entirely in wrong region; all downstream conclusions affected
- Major 2 (profile likelihood does not fix rho3 during optimization): A — rw.sd allows rho3 to drift; resulting profile and CI are invalid
- Major 3 (rw.sd boundaries systematically misaligned with covariate boundaries): A — piecewise parameters perturbed at wrong time steps
- Major 4 (SEIRS model fails to beat ARMA benchmark by large margin): A — 32.5 log-unit gap indicates misspecification or optimization failure
- Major 5 (profile CI unreliable and incomplete): A — coarse grid, boundary issue, and profiles absent for key parameters
- Major 6 (ESS collapse and conditional log-likelihood failures underdiagnosed): A — particle filter collapse not quantified or addressed
- Major 7 (no profile likelihoods for key biological parameters): A — mu_RS near zero left unexamined without formal identifiability test
- Minor (count error: text says 4 points, data shows 3): C — minor verifiable inaccuracy in profile description
- Minor (transmission rate notation inconsistency, alpha in text not in code): C — alpha appears in mathematical description but not in Csnippet
- Minor (ARMA(2,2) MA polynomial notation error, duplicate subscript): C — psi_1 used twice instead of psi_1 and psi_2
- Minor (W accumulator serves no purpose): C — state variable tracked but never used in measurement or diagnostics
- Minor (simulation uses simulate() not filtering distribution): C — forward simulation used for validation; filtering-conditioned simulation not presented
- Minor (population size not updated for current year): C — fixed N may not reflect population during 2020-2024
- Minor (periodogram interpretation incomplete): C — peak at frequency 0 does not preclude annual seasonality at 1/52
- Minor (no reproducibility documentation): C — no README, sessionInfo(), or renv lockfile
- Minor (local search convergence description imprecise): C — "converges around -1500" understates the 14 of 40 runs below that threshold

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed

**Findings classification:**
- Major 1 (global search initialized from previous mif2 result, not base pomp object): A — cooling schedule inherited; global search effectively re-evaluates local region
- Major 2 (profile for rho3 invalid: rho3 not held fixed during optimization): A — rw.sd allows rho3 to drift; 452 distinct values in saved artifact instead of 11
- Major 3 (particle filter failures underdiagnosed): A — ESS collapse and log-likelihood spikes indicate model-data mismatch not addressed
- Major 4 (implausible mu_RS treated as parameter choice not misspecification signal): A — near-zero waning rate should prompt nested SEIR comparison or identifiability analysis
- Major 5 (insufficient model diagnostics: no conditional log-likelihood decomposition, no filtering-distribution comparison): A — latent state trajectories and filtering simulations absent
- Major 6 (profile CI uses profile maximum rather than global maximum): A — cutoff raised by ~0.89 units, making CI anticonservative
- Major 7 (weak parameter identifiability acknowledged but not acted upon): A — broad ridges for most parameters; no remedial action taken
- Minor 8 (ARMA(2,2) duplicate subscript in equation): C — psi_1 written twice in MA polynomial
- Minor 9 (duplicate N column in profile results artifact): C — fixed_params N appended redundantly in c(guess, fixed_params)
- Minor 10 (force of infection in Csnippet drops alpha exponent): C — alpha in math specification absent from code without clarifying note
- Minor 11 (SEIRS fails to beat ARMA benchmark; gap not fully discussed): C — 32.5-unit gap attributed to pandemic difficulty without deeper examination
- Minor 12 (no model comparison between SEIR and SEIRS): C — formal LRT comparing mu_RS=0 restricted model not performed
- Minor 13 (reporting rate intervals inconsistent with transmission rate intervals): C — breakpoint at week 125 vs. week 72 not biologically motivated
- Minor 14 (initial conditions fixed rather than estimated, no sensitivity analysis): C — eta alone determines compartment initialization; E(0) and I(0) fixed at minimum
- Minor 15 (no sessionInfo() or package version documentation): C — reproducibility compromised by absent version information

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed

**Findings classification:**
- Major 1 (profile likelihood too sparse to support reported CI): A — only 4 points above threshold; upper bound at hard parameter boundary
- Major 2 (non-convergence pervasive but described as "not problematic"): A — b1, b2, b3, rho1-3, mu_EI, mu_RS, tau, sigmaSE all fail to converge in local search
- Minor 1 (measurement model uses H without defining it): C — variable H used in equation before being defined
- Minor 2 (procedure for obtaining final log-likelihood estimates not stated): C — whether replicated pfilter was used at mif2 endpoint left unstated
- Minor 3 (ESS collapse needs more specific attribution): C — collapse attributed generically to holidays; piecewise structure as cause not examined
- Minor 4 (mu_RS near zero should be framed as identifiability constraint, not misspecification): C — 4-year dataset cannot estimate 20-year rate; this is an identifiability issue
- Minor 5 (initial compartment allocations not stated): C — E(1), I(1), R(1) not explicitly documented given eta=0.89
- Minor 6 (AIC reasoning statement misframes relationship): C — "adding a parameter cannot decrease log-likelihood so AIC cannot increase by more than 2" is incorrect framing
- Minor 7 (importation parameter iota description incorrect): C — described as population flow rather than additional infectious pressure in force-of-infection

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 2 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 6 | 7 | 7 | 2 |
| B (AI major, human also found) | 0 | 0 | 0 | 0 |
| C (AI minor, human missed) | 9 | 9 | 8 | 7 |
| D (AI minor, human also found) | 0 | 0 | 0 | 0 |
| E (Human found, AI missed) | 2 | 2 | 2 | 2 |

---

## Per-Reviewer Metrics

Human Issues total: 2

- **Alex:** Human Recall = (B+D)/(B+D+E) = 0/(0+2) = 0.00 | AI-Unique Rate = (A+C)/(A+B+C+D) = 15/15 = 1.00
- **Charlie:** Human Recall = 0/(0+2) = 0.00 | AI-Unique Rate = 16/16 = 1.00
- **Doug:** Human Recall = 0/(0+2) = 0.00 | AI-Unique Rate = 15/15 = 1.00
- **Evan:** Human Recall = 0/(0+2) = 0.00 | AI-Unique Rate = 9/9 = 1.00

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #1 (vaccination not modeled): missed by all 4 reviewers
- Human Issue #2 (residuals centered around zero is mathematical necessity): missed by all 4 reviewers

Count: 2 out of 2 human issues (100%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others: none (all human issues were missed by every reviewer).

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |

### Universal AI-only flags

Issues raised by every reviewer that the human did not mention:

All AI findings in this project are AI-unique (no reviewer covered either human issue). The issues raised by all four reviewers in common include:

- Profile likelihood for rho3 is invalid / too sparse / rho3 not fixed during optimization (raised as Major by Alex, Charlie, Doug, and Evan)
- SEIRS model fails to outperform ARMA benchmark by ~32.5 log units (raised by Alex as Major, Charlie as Major, Doug as Minor, Evan implicitly via non-convergence discussion)
- Near-zero mu_RS estimate implies biologically implausible waning immunity period (~32 years) (raised as Major by Alex, Charlie, Doug; Minor by Evan)
- ESS collapse / particle filter failures underdiagnosed (raised as Moderate by Alex, Major by Charlie and Doug, Minor by Evan)
- sigmaSE at or beyond global search upper bound (raised as Major by Alex and Charlie)
- Parameter non-convergence pervasive and not adequately addressed (raised by all four reviewers)

Universal AI-only flag count: 6 distinct concerns raised by all or nearly all reviewers, none of which appeared in the human review.
