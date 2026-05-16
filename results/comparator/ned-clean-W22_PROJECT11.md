# Ned-Clean Analysis — W22 Project 11

---

## Human Issues

1. The outlier removal decisions seem reasonable, but county data reveal that some outliers are shared across counties, making it harder to explain them as data collection or processing errors.
2. The MIF2 diagnostics show that some searches essentially failed (green and cyan in the local search) — it might be clearer to remove them from subsequent analysis.
3. It would be useful to compare to an ARMA or log-ARMA benchmark likelihood to give some indication of whether substantial additional changes are required to reach a mechanistic model with good statistical fit.

---

## Alex

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Outliers are removed without statistical justification")
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "No comparison to a baseline model (e.g., SARIMA, simpler SIR, or null log-likelihood)")

**Findings classification:**
- Finding 1 (R update equation incorrect): A — recovered compartment updated via population-balance identity rather than differential flow
- Finding 2 (negative iota at MLE): A — iota allowed to go negative; force of infection becomes undefined
- Finding 3 (implausible R0 ~83 local, ~202 global): A — R0 and gamma far outside chickenpox biological range
- Finding 4 (outlier removal): B — no statistical justification for data removal (matches Human Issue #1)
- Finding 5 (global/local R0 range inconsistency): A — global search range [6,14] excludes local MLE of ~83; searches incoherent
- Finding 6 (alpha fixed but also perturbed): A — contradiction between estpars exclusion of alpha and rw.sd including alpha
- Finding 7 (no baseline comparison): B — no SARIMA or null log-likelihood benchmark reported (matches Human Issue #3)
- Finding 8 (single simulation replicate): A — nsim=1 in both evaluate calls; no uncertainty characterization
- Finding 9 (vaccination conflates with recovery): A — vaccination flows only from newborns, biological justification weak
- Finding 10 (duplicate rows in CSV) [Moderate]: C — same parameter set appears multiple times, inflating apparent search breadth
- Finding 11 (cooling fraction 0.1) [Moderate]: C — cooling.fraction.50=0.1 very aggressive; perturbations decay too fast
- Finding 12 (initial parameters from Birmingham measles) [Moderate]: C — sigma, gamma, amplitude etc. borrowed from measles without chickenpox-specific justification
- Finding 13 (rho justification circular) [Moderate]: C — rho computed as cases/births rather than cases/true infections
- Finding 14 (global MLE implausible values unremarked) [Moderate]: C — gamma=922 and iota=-0.43 presented without comment in global evaluation table
- Finding 15 (seasonality windows from English measles) [Minor]: C — school-term windows for England used for Hungary without adaptation

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 1 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Outlier removal not adequately justified")
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "No non-mechanistic benchmark comparison")

**Findings classification:**
- Finding 1 (implausible global MLE parameters accepted uncritically) [Major]: A — R0=202, gamma=922, iota=-0.429, rho=0.968 presented without diagnosis
- Finding 2 (negative iota used as nominal best-fit) [Major]: A — iota=-0.4295 in global MLE; pow(I+iota, alpha) undefined when iota<0
- Finding 3 (global < local likelihood, no resolution) [Major]: A — 77-unit gap acknowledged but not resolved
- Finding 4 (no non-mechanistic benchmark) [Major]: B — no ARMA/SARIMA comparison provided (matches Human Issue #3)
- Finding 5 (no formal profile likelihoods) [Major]: A — poor man's profile for vr is not a proper profile; no CIs for any parameter
- Finding 6 (cooling fraction 0.1 aggressive) [Major]: A — perturbations decay to negligible size early; likely causes premature convergence
- Finding 7 (large Monte Carlo SE in local search) [Major]: A — several runs have loglik.se values of 99.32, 14.31 etc.; estimates unreliable
- Finding 8 (local search R0 also implausible) [Minor]: C — R0=82.67 from local search far above literature range of 7-12
- Finding 9 (outlier removal not justified) [Minor]: D — no formal criterion for removing six observations (matches Human Issue #1)
- Finding 10 (global search fixes initial conditions) [Minor]: C — S_0, E_0, I_0, R_0 fixed at local MLE values in global search
- Finding 11 (single simulation trajectory) [Minor]: C — nsim=1 in both local and global evaluation; not informative about model uncertainty
- Finding 12 (iota lacks log transform in partrans) [Minor]: C — iota not log-transformed; optimizer can reach negative values silently
- Finding 13 (no ARIMA/spectral baseline for EDA) [Minor]: C — EDA shows time series and bar chart but no ACF/PACF or spectral analysis
- Finding 14 (eval=FALSE code errors) [Minor]: C — code references objects from non-evaluated blocks; reproducibility undermined
- Finding 15 (vaccination double-counts from S) [Minor]: C — R = pop - S - E - I + vac may not correctly track population balance

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 1 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Outlier removal without formal justification")
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "No non-mechanistic benchmark comparison")

**Findings classification:**
- Finding 1 (population conservation violated in R compartment) [Major]: A — R = pop - S - E - I + vac causes total population to grow by vac at each step
- Finding 2 (global search box misaligned with true MLE) [Major]: A — box sets R0 in [6,14] but MLE drifts to R0=202; only 1 of 400 replicates near global best
- Finding 3 (global search initialized from previous mif2 result) [Major]: A — mf1 passed as first argument inherits near-expired cooling schedule; cannot genuinely explore parameter space
- Finding 4 (global < local likelihood by 77 units) [Major]: A — result of box misalignment and anti-pattern initialization; global parameters not reliable MLEs
- Finding 5 (negative iota; potential NaN in force of infection) [Major]: A — 71 of 400 global replicates have negative iota; pow(negative, non-integer) yields NaN in C
- Finding 6 (no non-mechanistic benchmark) [Major]: B — no ARIMA/SARIMA/auto-regressive negative binomial baseline (matches Human Issue #3)
- Finding 7 (no profile likelihoods) [Major]: A — poor man's profile for vr not a genuine profile likelihood; no CIs for any parameter
- Finding 8 (implausible parameter estimates not interrogated) [Major]: A — R0=82.7 approximately 8x literature value; sigma=113 implies 3.2-day incubation vs. 10-21 days known
- Finding 9 (seasonality windows copied from UK measles) [Major]: A — English school-term windows used for Hungary without verification or adaptation
- Finding 10 (initial conditions fixed in global but estimated in local) [Minor]: C — global and local searches optimize different objectives; log-likelihoods not directly comparable
- Finding 11 (outlier removal without formal justification) [Minor]: D — six points removed as "possible data entry errors" without quantitative criterion (matches Human Issue #1)
- Finding 12 (normal approximation to negative binomial) [Minor]: C — dmeasure uses pnorm rather than dnbinom_mu; inaccurate for small expected counts
- Finding 13 (rho initialization incorrect) [Minor]: C — rho computed as cases/births, not cases/true infections; initialization rationale is wrong
- Finding 14 (cooling fraction aggressive) [Minor]: C — cooling.fraction.50=0.1 causes perturbations to decay to 0.1^8 of initial size by final iteration
- Finding 15 (global evaluation table biologically incoherent) [Minor]: C — gamma=922 (0.4-day recovery) and vr=0.62 (62% vaccination) presented without caveats

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 1 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Outlier removal without documented criterion")
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "No non-mechanistic benchmark")

**Findings classification:**
- C1 (no non-mechanistic benchmark) [Major]: B — no ARMA or SARIMA comparison provided (matches Human Issue #3)
- C2 (biologically implausible parameter estimates) [Major]: A — R0=82.67 local, R0=202 global; sigma implies 3-day latent period vs. known 10-21 days
- C3 (no proper profile likelihood or CIs) [Major]: A — poor man's profile for vr is scatter plot, not formal profile; no CIs for any parameter
- C4 (global search maximum 77 units below local) [Major]: A — gap acknowledged; computational explanation incomplete; global results exploratory only
- C5 (single forward simulation draw) [Major]: A — nsim=1 in figs. 10 and 13; single stochastic draw not informative about goodness-of-fit
- C6 (initial conditions fixed in global search) [Major]: A — mu, S_0, E_0, I_0, R_0 fixed from local MLE; may partly explain 77-unit gap
- C7 (negative iota in optimization) [Minor]: C — force-of-infection undefined when I+iota<0 with non-integer alpha; no log transform in partrans
- C8 (outlier removal without criterion) [Minor]: D — six weekly observations removed as "possible data entry errors" without stated criterion (matches Human Issue #1)
- C9 (run_level not stated in text) [Minor]: C — text never states which run_level was used for final reported results
- C10 (normal approximation not justified) [Minor]: C — dmeasure uses normal approximation; negative binomial more appropriate; choice not discussed
- M1 (vaccine effectiveness 0.92 hardcoded) [Minor]: C — estimated vr absorbs any misspecification of fixed 0.92; quantities not separately identified

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 1 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 7 | 6 | 8 | 5 |
| B (AI major, human also found) | 2 | 1 | 1 | 1 |
| C (AI minor, human missed) | 6 | 7 | 5 | 4 |
| D (AI minor, human also found) | 0 | 1 | 1 | 1 |
| E (Human found, AI missed) | 1 | 1 | 1 | 1 |

---

## Per-Reviewer Metrics

**Alex**
- Human Recall = (B+D) / (B+D+E) = (2+0) / (2+0+1) = 2/3 = 0.667
- AI-Unique Rate = (A+C) / (A+B+C+D) = (7+6) / (7+2+6+0) = 13/15 = 0.867

**Charlie**
- Human Recall = (B+D) / (B+D+E) = (1+1) / (1+1+1) = 2/3 = 0.667
- AI-Unique Rate = (A+C) / (A+B+C+D) = (6+7) / (6+1+7+1) = 13/15 = 0.867

**Doug**
- Human Recall = (B+D) / (B+D+E) = (1+1) / (1+1+1) = 2/3 = 0.667
- AI-Unique Rate = (A+C) / (A+B+C+D) = (8+5) / (8+1+5+1) = 13/15 = 0.867

**Evan**
- Human Recall = (B+D) / (B+D+E) = (1+1) / (1+1+1) = 2/3 = 0.667
- AI-Unique Rate = (A+C) / (A+B+C+D) = (5+4) / (5+1+4+1) = 9/11 = 0.818

---

## Cross-Reviewer Aggregation

**Consensus misses:** Human issues that every reviewer failed to cover.

- Human Issue #2: The MIF2 diagnostics show that some searches essentially failed (green and cyan in the local search) — it might be clearer to remove them from subsequent analysis. (Missed by all 4 reviewers — 1 out of 3 human issues, 33%)

**Unique finds per reviewer:** Human issues covered by only one reviewer (and missed by all others).

No human issue was covered by exactly one reviewer. Both covered human issues (HI#1 and HI#3) were found by all four reviewers.

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |

**Universal AI-only flags:** Issues raised by every reviewer that the human did not mention. (3 issues)

1. Negative iota constraint missing — the force-of-infection becomes undefined when I+iota<0 with non-integer alpha; iota should be constrained positive via a log transform in partrans. (Raised by all 4 reviewers; classified as Major by Alex, Charlie, Doug; Minor by Evan.)

2. Biologically implausible parameter estimates — R0 from the local search (~83) and global search (~202) far exceed the epidemiologically accepted range of 7–12 for chickenpox; similarly gamma and sigma values are inconsistent with known disease biology. (Raised by all 4 reviewers; classified as Major by all.)

3. Global search maximum lower than local search maximum by ~77 log-likelihood units — the global search fails to confirm or improve upon the local MLE, indicating either computational inadequacy or a fundamental problem with the search setup. (Raised by all 4 reviewers; classified as Major by all.)
