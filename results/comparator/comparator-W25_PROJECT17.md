# Comparator Analysis — W25 Project 17

---

## Human Issues

1. The modification of the SV for t-distributed returns (Sec 2.3) is described as a good decision, but the likelihood improves only a little and the estimated degrees of freedom for tau is quite large, which is surprising and warrants discussion.

2. The effective sample size diagnostics show occasional crashes even with the t-distributed tails, which is somewhat surprising.

3. The report identifies seasonality in gasoline prices, which is interesting, but then ignores this exploratory discovery by proceeding with models that do not include seasonality.

4. Various features of commodity prices are different from stocks — there is no economic principle against commodities autoregressing toward a fair market price or having seasonality, whereas the efficient market hypothesis suggests this is not true for stock market assets. GARCH and many of its generalizations cannot handle seasonality; this might be a case for SARMA with GARCH errors.

5. It would be good to comment on the computational requirements of all these experiments, as fitting POMP models usually requires substantial computation; this would also give insight to people wanting to reproduce the results.

6. This project uses monthly data, whereas volatility models are most commonly developed and used for higher-frequency data.

7. The authors should be more careful about language that may imply causation — the claim that government policies can affect the leverage effect requires more evidence given the complexity of the system.

8. The t degree of freedom parameter tau is described as being in the range [0, 60], but the convergence plots suggest that constraint is not enforced; additionally, tau is often sufficiently large that the t distribution should be very close to normal, which is worth discussion.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding 7: "No EDA beyond visual inspection — STL seasonality identified at end as diagnostic rather than at the start; seasonality should have been detected and discussed before model fitting")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding 15: "Hypothesis framing tied to regulatory narrative is weakly supported — evidence chain tenuous, conclusion overstates the strength of evidence for regulation limiting leverage")
- Human Issue #8: covered (matched by finding 5: "No parameter transformations for tau and amplitude; positivity constraints not enforced — tau can go negative or to zero without log transformation")

**Findings classification:**
- Finding 1 (Hard-coded regime-shift windows — data snooping): A — Major finding; human did not raise it
- Finding 2 (Missing daily data file prevents reproducibility): A — Major finding; human did not raise it
- Finding 3 (AIC selection inconsistency with final GARCH model fit): A — Major finding; human did not raise it
- Finding 4 (GARCH model labeling error T-GARCH(3,1) vs T-GARCH(1,3)): A — Major finding; human did not raise it
- Finding 5 (No parameter transformations for tau/amplitude; positivity not enforced): B — Major finding (matches Human Issue #8)
- Finding 6 (Leftover development comments in submitted code): C — Minor finding; human did not raise it
- Finding 7 (No EDA beyond visual inspection; seasonality found late not early): D — Minor finding (matches Human Issue #3)
- Finding 8 (AIC penalty adequacy — 1.4-unit difference not decisive): C — Minor finding; human did not raise it
- Finding 9 (Regime-amplitude parameter not consistently identified across models): C — Minor finding; human did not raise it
- Finding 10 (Rw.sd for tau disproportionately large relative to other parameters): C — Minor finding; human did not raise it
- Finding 11 (Equation 4 notation inconsistency between base and t-distribution models): C — Minor finding; human did not raise it
- Finding 12 (No simulation-based diagnostics for final SV models): C — Minor finding; human did not raise it
- Finding 13 (Filtered log-likelihood for simulated data is misleading): C — Minor finding; human did not raise it
- Finding 14 (Demeaning formula mismatch between equation and code): C — Minor finding; human did not raise it
- Finding 15 (Hypothesis framing tied to regulatory narrative weakly supported): D — Minor finding (matches Human Issue #7)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "Seasonal component detected by STL but not modeled in any POMP specification")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: covered (matched by finding: "tau and amplitude lack parameter transformations in partrans — optimizer may propose values ≤ 0, handled only by hard clamp that may not enforce the stated [0,60] range")

**Findings classification:**
- Finding 1 (Hard-coded regime shift — data snooping): A — hard-coded windows for 2008 and 2020 constitute data snooping invalidating AIC comparison
- Finding 2 (No profile likelihoods or CIs): A — no profile likelihood computations for any parameter
- Finding 3 (Inconsistent GARCH specification): A — AIC table uses include.mean=F but final log-likelihood comparison uses include.mean=T
- Finding 4 (Daily data file missing): A — required data file for Figure 2 absent from submission
- Finding 5 (MC variability not propagated into AIC): A — stochastic log-likelihood estimates used in borderline ΔAIC ≈ 1.4 comparison without SE reporting
- Finding 6 (Global search from single local result): A — all global searches initialized from if1[[1]] rather than fresh base object
- Finding 7 (tau and amplitude lack transformations in partrans): D — optimizer may propose invalid tau values, clamp may not enforce stated [0,60] constraint (matches Human Issue #8)
- Finding 8 (No non-mechanistic benchmark): C — no IID or ARMA baseline for SV models
- Finding 9 (Seasonal component not modeled): D — STL reveals seasonality that is identified but not incorporated into any POMP model (matches Human Issue #3)
- Finding 10 (Base vs modified SV not formally compared): C — ~7 log-likelihood unit improvement described qualitatively without AIC table entry
- Finding 11 (epsilon_n not in model equations): C — epsilon_n mentioned in text but absent from equations (1)–(4)
- Finding 12 (No EDA section): C — report moves from introduction directly to model specification without dedicated EDA
- Finding 13 (Parameter perturbation sizes not discussed): C — rw.sd=1.0 for tau vs 0.02 for other parameters not justified
- Finding 14 (Conclusions overstate statistical evidence): C — ΔAIC ≈ 1.4 presented as supporting leverage hypothesis without formal test
- Finding 15 (fGarch log-likelihood normalization not verified): C — fGarch log-likelihood compared to POMP particle filter without checking normalization convention

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: covered (matched by finding: "tau and amplitude parameters lack partrans declarations — tau constraint [0,60] not enforced in IF2 optimization")

**Findings classification:**
- Major #1 (global search wrong anchor — mif2(if1[[1]]) instead of base pomp object): A — global search inherits decayed cooling schedule, no genuine exploration
- Major #2 (SV vs GARCH log-likelihood comparison invalid): A — different observation models, unequal degrees of freedom, Jacobian equivalence unverified
- Major #3 (hardcoded event windows — look-ahead bias): A — event intervals and multipliers derived from visual data inspection, not estimated
- Major #4 (initial log-likelihoods computed on simulated data, not real data): A — values 410.657, 457.797, 472.035 are on model-simulated output, not actual gasoline returns
- Major #5 (no profile likelihoods for any parameter): A — leverage hypothesis rests on qualitative reading of pairs plot, no formal CI for sigma_nu
- Major #6 (no non-mechanistic benchmark comparison): A — GARCH comparison is methodologically compromised; no ARMA or AR(p)-t baseline
- Major #7 (tau and amplitude lack parameter transformation declarations): B — IF2 can push tau below zero; clamping silently distorts optimization; [0,60] constraint not properly enforced (matches Human Issue #8)
- Major #8 (AIC table uses hardcoded log-likelihoods): A — values not extracted from live R objects, table will not update on rerun
- Major #9 (inadequate diagnostics — no conditional log-likelihood plot): A — only ESS traces and pairs plots; no per-observation likelihood decomposition
- Major #10 (daily data loaded only for visualization, missing file dependency): A — daily CSV absent from submission, no daily analysis performed
- Minor (simulated log-likelihood notation mismatch — sigma_nu sign): C — code sets exp(-4.5) but text states exp(4.5)
- Minor (tau rw.sd = 1 is disproportionately large): C — 20% of starting value vs. 0.02 for other parameters, compounded by integer clamping
- Minor (write.table appending in eval=FALSE chunks — vestigial code): C — CSV accumulation never executed or read back
- Minor (GARCH AIC tie-breaking ambiguity in which.min logic): C — undefined behavior if two models tie
- Minor (STL decomposition applied to log-returns not squared returns): C — does not directly show volatility seasonality; stated conclusion unsupported
- Minor (parameter estimates not reported in any table): C — best-fit parameters inferrable only from pairs plots
- Minor (missing daily CSV file): C — document will fail to render without Daily_New_York_Harbor file

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 9 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "25.17.14 — Seasonal pattern unmodeled")
- Human Issue #4: covered (matched by finding: "25.17.6 — No mean-model baseline (ARMA/SARIMA)" and "25.17.14 — Seasonal pattern unmodeled")
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed

**Findings classification:**
- 25.17.1: A — mif2 internal log-likelihood likely used in AIC table; no replicated pfilter runs or Monte Carlo SEs reported
- 25.17.3: A — hard-coded regime windows introduce data-snooping bias, confounding the leverage hypothesis test
- 25.17.4: A — no profile likelihoods computed for any model parameter, leaving identifiability unassessed
- 25.17.6: B — no mean-model baseline (ARMA/SARIMA); STL decomposition reveals seasonality that should be addressed before variance modeling (matches Human Issue #4)
- 25.17.14: D — seasonal pattern identified in STL decomposition but not incorporated into any POMP model (matches Human Issues #3 and #4)
- 25.17.2: C — GARCH vs. SV likelihood scale comparison lacks explicit confirmation of matching normalizing conventions
- 25.17.M1: C — no simulation-based diagnostics for POMP models, unlike the QQ-plot and ACF provided for GARCH
- 25.17.M2: C — initial conditions G_0 = H_0 = 0 fixed without justification or sensitivity analysis

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 3 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 4 | 6 | 9 | 3 |
| B (AI major, human also found) | 1 | 0 | 1 | 1 |
| C (AI minor, human missed) | 8 | 7 | 7 | 3 |
| D (AI minor, human also found) | 2 | 2 | 0 | 1 |
| E (Human found, AI missed) | 5 | 6 | 7 | 6 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 1 | 2 | 5 | 3/8 = 38% | 4 | 8 | 12/15 = 80% |
| Charlie | 0 | 2 | 6 | 2/8 = 25% | 6 | 7 | 13/15 = 87% |
| Doug | 1 | 0 | 7 | 1/8 = 12% | 9 | 7 | 16/17 = 94% |
| Evan | 1 | 1 | 6 | 2/8 = 25% | 3 | 3 | 6/8 = 75% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #1: The modification of the SV for t-distributed returns (Sec 2.3) is described as a good decision, but the likelihood improves only a little and the estimated degrees of freedom for tau is quite large, which is surprising and warrants discussion. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #2: The effective sample size diagnostics show occasional crashes even with the t-distributed tails, which is somewhat surprising. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #5: It would be good to comment on the computational requirements of all these experiments, as fitting POMP models usually requires substantial computation; this would also give insight to people wanting to reproduce the results. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #6: This project uses monthly data, whereas volatility models are most commonly developed and used for higher-frequency data. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 4 out of 8 human issues (50%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #4: Various features of commodity prices are different from stocks — there is no economic principle against commodities autoregressing toward a fair market price or having seasonality, whereas the efficient market hypothesis suggests this is not true for stock market assets. GARCH and many of its generalizations cannot handle seasonality; this might be a case for SARMA with GARCH errors. (Covered only by Evan)
- Human Issue #7: The authors should be more careful about language that may imply causation — the claim that government policies can affect the leverage effect requires more evidence given the complexity of the system. (Covered only by Alex)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 1 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 1 |
