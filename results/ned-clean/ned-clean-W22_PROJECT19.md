# Ned-Clean Analysis — W22 Project 19

---

## Human Issues

1. If you want to difference the data, 7-day differencing would remove the weekly periodicity. One could sum up cases over each week as another way to avoid dealing with day-of-week effects. This is simpler than the idea proposed in the conclusion of explicitly modeling day of week as a covariate.
2. Shapiro-Wilk test does not add much to the QQ plot here. The QQ plot tells you the nature of the non-normality (long tails both ends) which Shapiro-Wilk does not.
3. You reject the null hypothesis that the postulated model is reasonable, and then say "therefore, the model can be represented by ..." which is not a clear conclusion.
4. It could be worth estimating E(t_0) and/or I(t_0) rather than fixing them. The model seems to struggle at the start of the wave.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "Hard-coded, unjustified initial conditions for E and I")

**Findings classification:**
- Finding 1 — Unfair log-likelihood comparison between ARIMA and SEIR: A (Major, human missed)
- Finding 2 — Data subsetting inconsistency: title says March 31 but code filters to February 28: A (Major, human missed)
- Finding 3 — Hard-coded, unjustified initial conditions for E and I: B (Major, matches Human Issue #4)
- Finding 4 — mu_EI and mu_IR fixed without adequate justification: A (Major, human missed)
- Finding 5 — Profile likelihood for tau unreliable: only two points above threshold, misreported CI: A (Major, human missed)
- Finding 6 — Global search finds beta2 < beta1, contradicting model motivation, not adequately investigated: A (Major, human missed)
- Finding 7 — Inadequate particle count and iteration count for reliable inference: A (Major, human missed)
- Finding 8 — ARIMA near-cancellation of AR and MA roots (Moderate): C (Minor, human missed)
- Finding 9 — Shapiro-Wilk test rejection not acted upon (Moderate): C (Minor, human missed)
- Finding 10 — Detected 7-day periodicity not incorporated into either model (Moderate): D (Minor, matches Human Issue #1)
- Finding 11 — Covariate intervention split (day 17) fixed and not estimated (Moderate): C (Minor, human missed)
- Finding 12 — Profile likelihood for tau only; no profiles for other parameters (Moderate): C (Minor, human missed)
- Finding 13 — Measurement model notation error: C (Minor, human missed)
- Finding 14 — ARIMA AIC table presented without full table visible: C (Minor, human missed)
- Finding 15 — Acknowledgements reveals structural similarity to prior projects, not cited: C (Minor, human missed)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "Initial conditions E = 6000 and I = 15000 fixed without justification or sensitivity analysis")

**Findings classification:**
- Finding 1 — Accumvar H never reset, measurement model uses cumulative count (bug): A (Major, human missed)
- Finding 2 — mu_EI and mu_IR fixed, identifiability not assessed: A (Major, human missed)
- Finding 3 — Profile likelihood for tau has only two points above Wilks threshold: A (Major, human missed)
- Finding 4 — Global search reveals beta2 < beta1 at MLE, contradicting model motivation: A (Major, human missed)
- Finding 5 — ARIMA and SEIR log-likelihoods compared without accounting for different observation models: A (Major, human missed)
- Finding 6 — Missing convergence diagnostics for global search: A (Major, human missed)
- Finding 7 — rw.sd settings inconsistent with parameter transformations: C (Minor, human missed)
- Finding 8 — Spectral analysis misidentifies dominant period (90-day vs. actual frequency): C (Minor, human missed)
- Finding 9 — Initial conditions E = 6000 and I = 15000 fixed without justification: D (Minor, matches Human Issue #4)
- Finding 10 — Measurement model notation ambiguity (H reused for latent and observed): C (Minor, human missed)
- Finding 11 — ARIMA model selection: near-cancelling roots not resolved: C (Minor, human missed)
- Finding 12 — Residual non-normality noted but not acted upon: C (Minor, human missed)
- Finding 13 — No non-mechanistic benchmark comparison for SEIR model: C (Minor, human missed)
- Finding 14 — Profile likelihood starting points create non-uniform grid: C (Minor, human missed)
- Finding 15 — Data subsetting inconsistency (Feb 28 vs. Mar 31): C (Minor, human missed)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "Fixed and biologically unmotivated initial conditions for E and I")

**Findings classification:**
- Finding 1 — Invalid log-likelihood comparison: different datasets and different observation models: A (Major, human missed)
- Finding 2 — Accumulator variable tracks wrong epidemiological event (dN_IR instead of dN_EI): A (Major, human missed)
- Finding 3 — Global search inherits cooling schedule from local search (anti-pattern): A (Major, human missed)
- Finding 4 — Profile likelihood neither globally seeded nor valid: 20-unit gap from global MLE: A (Major, human missed)
- Finding 5 — Profile CI displayed with incorrect units (code bug): A (Major, human missed)
- Finding 6 — No comparison to non-mechanistic benchmark on same data: A (Major, human missed)
- Finding 7 — Fixed and biologically unmotivated initial conditions for E and I: B (Major, matches Human Issue #4)
- Finding 8 — Key epidemiological parameters mu_EI and mu_IR fixed without sensitivity analysis: A (Major, human missed)
- Finding 9 — Global MLE contradicts paper's key biological claim (beta2 < beta1): A (Major, human missed)
- Minor — ARIMA(4,1,4) overparameterized: C (Minor, human missed)
- Minor — Residual normality rejected but no action taken: C (Minor, human missed)
- Minor — Data description inconsistency (intro vs. code date range): C (Minor, human missed)
- Minor — Profile starts stratified by tau but IF2 base object wrong: C (Minor, human missed)
- Minor — Measurement model notation inconsistency: C (Minor, human missed)
- Minor — No model diagnostics beyond visual fit: C (Minor, human missed)
- Minor — No forecast methodology: C (Minor, human missed)
- Minor — Computation level insufficient given convergence gaps: C (Minor, human missed)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "22.19.m3 — Shapiro-Wilk applied after QQ plot already shows non-normality")
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "22.19.m1 — Initial conditions E = 6000 and I = 15000 hard-coded")

**Findings classification:**
- 22.19.M1 — Log-likelihood comparison not scale-valid: A (Major, human missed)
- 22.19.M2 — Profile tau too sparse, CI meaningless; code bug displays tau as percentage: A (Major, human missed)
- 22.19.M3 — Beta2 severely unstable, consistent with non-identifiability: A (Major, human missed)
- 22.19.M4 — Particle count and NMIF values never reported in manuscript: A (Major, human missed)
- 22.19.M5 — No standard POMP diagnostics (ESS, conditional log-likelihoods): A (Major, human missed)
- 22.19.M6 — mu_EI and mu_IR fixed without sensitivity analysis: A (Major, human missed)
- 22.19.m1 — Initial conditions E = 6000 and I = 15000 hard-coded, not estimated: D (Minor, matches Human Issue #4)
- 22.19.m2 — Biological interpretation "Omicron not as contagious" unsupported given beta2 instability: C (Minor, human missed)
- 22.19.m3 — Shapiro-Wilk applied redundantly after QQ plot already shows non-normality: D (Minor, matches Human Issue #2)
- 22.19.m4 — 90-day spectral peak misidentified as cyclic phenomenon rather than trend artifact: C (Minor, human missed)
- 22.19.m5 — Figures lack captions: C (Minor, human missed)
- 22.19.m6 — ARIMA(4,1,4) near-canceling AR and MA roots: C (Minor, human missed)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 6 | 6 | 8 | 6 |
| B (AI major, human also found) | 1 | 0 | 1 | 0 |
| C (AI minor, human missed) | 8 | 8 | 7 | 4 |
| D (AI minor, human also found) | 1 | 1 | 0 | 2 |
| E (Human found, AI missed) | 2 | 3 | 3 | 2 |

---

## Per-Reviewer Metrics

**Alex**
- Human Recall = (B+D) / (B+D+E) = (1+1) / (1+1+2) = 2/4 = **0.50**
- AI-Unique Rate = (A+C) / (A+B+C+D) = (6+8) / (6+1+8+1) = 14/16 = **0.875**

**Charlie**
- Human Recall = (B+D) / (B+D+E) = (0+1) / (0+1+3) = 1/4 = **0.25**
- AI-Unique Rate = (A+C) / (A+B+C+D) = (6+8) / (6+0+8+1) = 14/15 = **0.933**

**Doug**
- Human Recall = (B+D) / (B+D+E) = (1+0) / (1+0+3) = 1/4 = **0.25**
- AI-Unique Rate = (A+C) / (A+B+C+D) = (8+7) / (8+1+7+0) = 15/16 = **0.938**

**Evan**
- Human Recall = (B+D) / (B+D+E) = (0+2) / (0+2+2) = 2/4 = **0.50**
- AI-Unique Rate = (A+C) / (A+B+C+D) = (6+4) / (6+0+4+2) = 10/12 = **0.833**

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #1: 7-day differencing as a simpler remedy for weekly periodicity (all four missed)
- Human Issue #3: Rejecting the null hypothesis and then drawing a positive conclusion ("model can be represented by...") is logically inconsistent (all four missed)

**Count: 2 out of 4 human issues (50%)**

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Alex: none
- Charlie: none
- Doug: none
- Evan: Human Issue #2 (Shapiro-Wilk adds nothing beyond the QQ plot)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 1 |

### Universal AI-only flags

Issues raised by every reviewer that the human did not mention:

1. Invalid log-likelihood comparison between ARIMA and SEIR (different observation models, different data; raised by all four as Major)
2. mu_EI and mu_IR fixed without sensitivity analysis (raised by all four as Major)
3. Profile likelihood for tau too sparse to yield a reliable confidence interval (raised by all four as Major)
4. Global search finds beta2 < beta1, contradicting the stated biological motivation, without adequate investigation (raised by all four as Major)
5. ARIMA(4,1,4) near-canceling AR and MA inverse roots suggesting over-parameterization (raised by all four as Minor/Moderate)

**Count: 5 universal AI-only flags**
