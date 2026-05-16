# Ned-Clean Analysis — w24 Project 08

---

## Human Issues

1. ARMA modeling would be more successful on the log scale.
2. The residual plot for ARMA shows dramatic heteroskedasticity. When the authors say "We can observe certain stationarity and good fit for this model," they are failing to see the information in the plot.
3. Early figures are numbered, but later figures are missing numbers and captions.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "ARIMA(3,1,3) selected despite non-normal residuals, no diagnostic follow-up — authors move on without investigation")
- Human Issue #3: missed

**Findings classification:**
- Issue 1 (MAJOR — wrong dataset SEIR): A — SEIR section fitted to Washtenaw County data, not King County
- Issue 2 (MAJOR — SVEIPR worse LL): A — SVEIPR log-likelihood ~182 units worse than SEIR, no discussion
- Issue 3 (MAJOR — double differencing): A — data already once-differenced, ARIMA applies second difference, effectively ARIMA(3,2,3)
- Issue 4 (MAJOR — reinfection bug): A — dN_RS drawn from I instead of R, corrupts reinfection mechanism
- Issue 5 (MAJOR — Euler step size): A — SVEIPR uses delta.t=1 (weekly), too coarse for rates as large as mu_EPI~1.3/week
- Issue 6 (MAJOR — LL comparison inconsistent): A — local vs global SVEIPR improvement of ~20 units described as insignificant
- Issue 7 (MODERATE — H accumulator): C — H only counts I→R transitions, excluding P→R, making alpha unidentifiable
- Issue 8 (MODERATE — c4 implausible values): C — best-fit c4 reaches 207–316, biologically implausible vaccination rates
- Issue 9 (MODERATE — SEIR poorly identified): C — beta values spanning 0.16 to 114,712, 67/100 NA log-likelihoods
- Issue 10 (MODERATE — profile CIs not computed): C — "poor man's profile" CIs described but not implemented correctly
- Issue 11 (MODERATE — key parameters not estimated): C — mu_RS, alpha, Beta, mu_SV fixed in local search, novel features never compared to data
- Issue 12 (MODERATE — non-normal residuals no follow-up): D — heavy-tailed residuals noted but authors move on; authors claim good fit without addressing diagnostics (matches Human Issue #2)
- Issue 13 (MINOR — LL value inconsistent): C — text states -1195.194 but stored data shows -1195.915
- Issue 14 (MINOR — initial conditions implausible): C — E=1000, I=500, P=500 at week 1 inconsistent with King County epidemiological context
- Issue 15 (MINOR — bibliography duplicates): C — several bib entries duplicated verbatim

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "EDA stationarity conclusion is overclaimed — authors conclude stationarity without formal test, non-stationarity of variance not addressed")
- Human Issue #3: missed

**Findings classification:**
- Major Issue 1 (dataset substitution bug): A — SEIR section silently uses Washtenaw County, Michigan data
- Major Issue 2 (reinfection coding error): A — dN_RS drawn from I instead of R, wrong sign in state update
- Major Issue 3 (no ARIMA vs POMP comparison): A — no quantitative comparison between ARIMA and POMP log-likelihoods
- Major Issue 4 (no profile likelihoods): A — no profile likelihoods or formal CIs for any parameter
- Major Issue 5 (parameters fixed without justification): A — seven parameters fixed in SVEIPR global search without epidemiological justification
- Major Issue 6 (insufficient SEIR computational effort): A — Np=200, Nmif=50 for SEIR global search, large loglik SEs
- Major Issue 7 (goodness-of-fit purely visual): A — no quantitative GOF statistics for SVEIPR, only simulation plots
- Major Issue 8 (measurement model inconsistency): A — SEIR uses negative binomial, SVEIPR uses Gaussian approximation without justification
- Minor — negative weekly case counts: C — differenced cumulative counts produce some negative values, not handled
- Minor — rm(list=ls()) code quality: C — clearing workspace mid-document indicates poor code organization
- Minor — ARIMA double differencing: C — sea_df$cases already differenced, arima(d=1) applies a second difference
- Minor — vaccination transition density-dependent: C — (I+P)/N multiplier means no vaccination at pandemic start when I+P≈0
- Minor — Beta fixed at 1.01: C — Beta and b_i individually unidentifiable since Beta is not optimized
- Minor — no seed documented for SVEIPR global: C — parallel RNG stream state not recorded, reproducibility uncertain
- Minor — poor man's CI informal: C — range of global search results not equivalent to proper profile likelihood
- Minor — EDA stationarity overclaimed: D — authors conclude stationarity from ACF without formal test, non-stationarity of variance ignored (matches Human Issue #2)
- Minor — sveipr_model.png missing: C — model diagram referenced but file not found in submission
- Minor — bibliography duplicates: C — multiple citation keys repeated verbatim

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "Figures 19, 20, 21 lack axis labels and captions explaining what parameter combinations are shown")

**Findings classification:**
- Major Issue 1 (wrong dataset): A — SEIR fitted on Washtenaw County, Michigan data
- Major Issue 2 (global search anti-pattern): A — SVEIPR global search inherits exhausted cooling schedule from local IF2 result
- Major Issue 3 (SVEIPR worse LL): A — SVEIPR ~182 LL units worse than SEIR, not acknowledged
- Major Issue 4 (dN_RS coding error): A — reinfection drawn from I instead of R, R compartment does not conserve mass
- Major Issue 5 (no benchmark comparison): A — ARIMA LL never compared to POMP LL quantitatively
- Major Issue 6 (parameter identifiability crisis): A — c4 ranges 0.28–316.9, b7/b8 orders of magnitude wide, flat likelihood
- Major Issue 7 (H accumulator excludes P→R): A — accumulator H only tracks I→R, P→R invisible to likelihood
- Major Issue 8 (SEIR global: 67/100 NA): A — severe particle degeneracy, only 33/100 runs produce plausible results
- Minor Issue 9 (ARIMA double differencing): C — data already once-differenced, d=1 in arima() creates double-differencing
- Minor Issue 10 (Gaussian approximation): C — SVEIPR measurement model uses Gaussian with no justification vs SEIR negative binomial
- Minor Issue 11 (high LL SE in SEIR local): C — loglik.se up to 10.69, estimates too noisy for reliable optimization
- Minor Issue 12 (fixed parameters): C — mu_PR, mu_IR, mu_RS, alpha fixed without biological references
- Minor Issue 13 (poor man's profile): C — range of global search runs not equivalent to profile likelihood
- Minor Issue 14 (no model diagnostics): C — no conditional log-likelihoods or ESS plots for best-fit model
- Minor Issue 15 (no forecast): C — stated goal of prediction not addressed, no out-of-sample evaluation
- misc-1 (figures lack axis labels and captions): D — Figures 19, 20, 21 lack axis labels and captions (matches Human Issue #3)
- misc-2 (initial conditions implausible): C — E=1000, I=500, P=500 at week 1 inconsistent with King County context

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "Figures 19, 20, 21 lack axis labels and captions explaining what parameter combinations are shown")

**Findings classification:**
- 24.08.1 (MAJOR — reinfection bug): A — dN_RS drawn from I instead of R, R grows without bound
- 24.08.2 (MAJOR — SVEIPR worse LL): A — SVEIPR ~183 LL units worse than SEIR, reversal unexplained
- 24.08.3 (MAJOR — parameters fixed without justification): A — seven parameters fixed ad hoc, Beta and b_i individually unidentifiable
- 24.08.5 (MAJOR — poor man's profile CIs): A — threshold not stated, no formal statistical meaning
- 24.08.6 (MAJOR — Gaussian measurement model): A — switch from negative binomial (SEIR) to Gaussian (SVEIPR) without justification
- 24.08.7 (MAJOR — double differencing): A — data processing conflates two distinct operations, second difference unnecessary if incidence already computed
- 24.08.8 (MAJOR — mu_IR implausible): A — SEIR best-fit mu_IR=5.33/week implies 1.3-day infectious period, biologically implausible for COVID-19
- 24.08.9 (MINOR — convergence overclaimed): C — several chains collapse but convergence called "successful"
- 24.08.4 minor (ARIMA and SEIR LL not comparable): C — ARIMA and POMP likelihoods computed on different data transformations
- 24.08.13 minor (run_level not documented): C — computational settings for reported results not stated in rendered output
- misc-1 (MINOR — figures lack captions): D — Figures 19, 20, 21 lack axis labels and captions (matches Human Issue #3)
- misc-2 (MINOR — initial conditions implausible): C — E=1000, I=500, P=500 inconsistent with King County epidemiological context

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 6 | 8 | 8 | 7 |
| B (AI major, human also found) | 0 | 0 | 0 | 0 |
| C (AI minor, human missed) | 8 | 9 | 8 | 4 |
| D (AI minor, human also found) | 1 | 1 | 1 | 1 |
| E (Human found, AI missed) | 2 | 2 | 2 | 2 |

---

## Per-Reviewer Metrics

Human Recall = (B + D) / (B + D + E)
AI-Unique Rate = (A + C) / (A + B + C + D)

| Reviewer | B+D | B+D+E | Human Recall | A+C | A+B+C+D | AI-Unique Rate |
|----------|----:|------:|-------------:|----:|---------:|---------------:|
| Alex | 1 | 3 | 33.3% | 14 | 15 | 93.3% |
| Charlie | 1 | 3 | 33.3% | 17 | 18 | 94.4% |
| Doug | 1 | 3 | 33.3% | 16 | 17 | 94.1% |
| Evan | 1 | 3 | 33.3% | 11 | 12 | 91.7% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #1: ARMA modeling would be more successful on the log scale — missed by all 4 reviewers.
- Human Issue #2: Residual plot for ARMA shows dramatic heteroskedasticity, authors claim good fit — missed by Doug and Evan; covered (partially) by Alex and Charlie via related residual diagnostic concerns.

Strict consensus misses (missed by ALL four reviewers): 1 out of 3 (33%).

Human Issue #1 is the only true consensus miss — no reviewer mentioned the log-scale transformation for ARMA modeling.

Human Issue #2 is a near-consensus miss: Alex and Charlie each partially addressed residual diagnostic concerns (non-normal residuals, overclaiming stationarity), which were counted as matching, but Doug and Evan missed it entirely.

Human Issue #3 was covered by Doug and Evan (figure captions) but missed by Alex and Charlie.

### Unique finds per reviewer

Human issues covered by only one reviewer and missed by all others:

- Human Issue #2 (ARMA residual heteroskedasticity): covered by Alex only (among those who matched it)
- Human Issue #2 (ARMA residual heteroskedasticity): also covered by Charlie

(Both Alex and Charlie independently matched Human Issue #2; neither Doug nor Evan did.)
- Human Issue #3 (missing figure captions): covered by Doug and Evan; missed by Alex and Charlie.

No human issue was covered by exactly one reviewer and missed by all others.

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |

### Universal AI-only flags

Issues raised as Major by every reviewer that the human did not mention:

All four reviewers flagged all of the following as Major (or equivalent), none mentioned by the human:

1. SEIR fitted to wrong dataset (Washtenaw County, Michigan) — flagged by Alex, Charlie, Doug (all as Major; Evan does not flag this one explicitly as a standalone major — wait, Evan does NOT include the wrong-dataset bug as a finding at all). Let me verify.

Looking at Evan's review again: the Overall Assessment mentions "a counterproductive reversal in which the more complex SVEIPR model achieves a substantially worse log-likelihood," and Key Strengths section mentions no wrong-dataset issue. Evan's Major Points are 24.08.1 through 24.08.8. None of these is the wrong-dataset bug. Evan misses the wrong-dataset finding entirely.

So the wrong-dataset bug is NOT flagged by Evan.

Issues raised as Major by all four reviewers:
- Reinfection coding error (dN_RS from I instead of R): Alex Issue 4 (MAJOR), Charlie Major Issue 2, Doug Major Issue 4, Evan 24.08.1 (MAJOR). All four. Human missed.
- SVEIPR worse LL than SEIR, not discussed: Alex Issue 2 (MAJOR), Charlie... actually Charlie does not have this as a standalone major. Let me check — Charlie's Major Issues are 1-8. Issue 3 is "No quantitative comparison between ARIMA and POMP models" — this is related but different from SVEIPR worse LL. Charlie's review summary mentions it but it may not be a standalone Major Issue. Looking at Charlie's majors: 1=dataset bug, 2=reinfection bug, 3=no ARIMA/POMP comparison, 4=no profile likelihoods, 5=parameters fixed, 6=insufficient computational effort, 7=GOF purely visual, 8=measurement model inconsistency. Charlie does not have a standalone Major Issue about SVEIPR LL being worse than SEIR. Doug has Major Issue 3 (SVEIPR worse LL). Evan has 24.08.2 (MAJOR). Alex has Issue 2 (MAJOR). So 3 out of 4 (Alex, Doug, Evan) flag this; Charlie addresses the related benchmark comparison but not the LL reversal directly.

Issues raised as Major by all four reviewers (human missed):
- Reinfection coding error (dN_RS from I instead of R): all 4 reviewers, all Major. Human missed. Count: 1 universal AI-only Major flag.

Additional issues raised as Major by 3 of 4:
- SVEIPR worse LL than SEIR: Alex, Doug, Evan (3/4)
- Wrong dataset in SEIR: Alex, Charlie, Doug (3/4; Evan misses it)
- Parameters fixed without justification: Charlie, Doug, Evan (3/4; Alex covers it as Moderate)
- No profile likelihoods/CIs: Charlie, Evan (2/4 as Major; Alex as Moderate, Doug as Minor)

Universal AI-only flags (Major, all 4 reviewers): 1 issue
- The reinfection coding bug (dN_RS drawn from I instead of R)
