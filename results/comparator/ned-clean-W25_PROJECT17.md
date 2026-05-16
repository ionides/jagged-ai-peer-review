# Ned-Clean Analysis — W25 Project 17

---

## Human Issues

1. The ESS diagnostics show occasional crashes even with t-distributed tails; the report notes this limitation without resolving it.
2. The report identifies seasonality in gasoline prices but then ignores this in subsequent models that do not include seasonality.
3. Computational requirements of the experiments are not discussed; commenting on them would aid reproducibility.
4. The project uses monthly data, whereas volatility models are most commonly developed and used for higher-frequency data.
5. The language may imply causation (e.g., government policies causing leverage effects) without sufficient evidence.
6. The tau degree-of-freedom parameter is described as being in the range [0,60] but the convergence plots suggest this constraint is not enforced; when tau is large, the t-distribution approaches normal, which is worth discussing.

---

## Alex

**Coverage record:**
- Human Issue #1 (ESS crashes persist with t-tails): missed
- Human Issue #2 (seasonality identified but ignored in models): covered (matched by finding: "no EDA beyond visual inspection; STL seasonality placed as afterthought rather than before model fitting")
- Human Issue #3 (computational requirements not discussed): missed
- Human Issue #4 (monthly data; volatility models usually higher-frequency): missed
- Human Issue #5 (causation language): missed
- Human Issue #6 (tau range not enforced; large tau approaches normal): covered (matched by finding: "no parameter transformations for tau/amplitude; positivity constraints not enforced")

**Findings classification:**
- Finding #1 (hard-coded regime-shift windows constitute data snooping): A — Major, human did not raise this
- Finding #2 (missing daily data file prevents full reproducibility): A — Major, human did not raise this
- Finding #3 (AIC selection vs. final GARCH model inconsistency: include.mean=F vs include.mean=T): A — Major, human did not raise this
- Finding #4 (GARCH model labeling error: T-GARCH(3,1) vs T-GARCH(1,3)): A — Major, human did not raise this
- Finding #5 (no parameter transformations for tau and amplitude; positivity constraints not enforced): B — Major, matches Human Issue #6
- Finding #6 (leftover development comments in submitted code): C — Minor, human did not raise this
- Finding #7 (no EDA beyond visual inspection; seasonality identified late as GARCH diagnostic): D — Minor, matches Human Issue #2
- Finding #8 (AIC comparison: small difference of 1.4 units not discussed; inadequate penalty discussion): C — Minor, human did not raise this
- Finding #9 (global search box misalignment: sigma_eta start outside box): C — Minor, human did not raise this
- Finding #10 (rw.sd for tau disproportionately large relative to other parameters): C — Minor, human did not raise this
- Finding #11 (Equation 4 notation: sigma_n conflated between base and t-distribution model): C — Minor, human did not raise this
- Finding #12 (no simulation-based diagnostics for final SV models): C — Minor, human did not raise this
- Finding #13 (filtered log-likelihood reported for simulated data is misleading): C — Minor, human did not raise this
- Finding #14 (demeaning formula mismatch between equation and code): C — Minor, human did not raise this
- Finding #15 (hypothesis framing tied to regulatory narrative is weakly supported): C — Minor, human did not raise this

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1 (ESS crashes persist with t-tails): missed
- Human Issue #2 (seasonality identified but ignored in models): missed
- Human Issue #3 (computational requirements not discussed): covered (matched by finding: "computational settings not reported in text")
- Human Issue #4 (monthly data; volatility models usually higher-frequency): missed
- Human Issue #5 (causation language): missed
- Human Issue #6 (tau range not enforced; large tau approaches normal): covered (matched by finding: "tau and amplitude lack parameter transformations; positivity not enforced")

**Findings classification:**
- Major #1 (global search anti-pattern: all three models initialize from previous IF2 result): A — Major, human did not raise this
- Major #2 (hard-coded structural breaks constitute look-ahead bias): A — Major, human did not raise this
- Major #3 (no profile likelihoods or confidence intervals for any parameter): A — Major, human did not raise this
- Major #4 (tau rw.sd = 1 is grossly misscaled): A — Major, human did not raise this
- Major #5 (tau and amplitude lack parameter transformations): B — Major, matches Human Issue #6
- Major #6 (AIC comparison between SV and GARCH models invalid across frameworks): A — Major, human did not raise this
- Major #7 (GARCH grid search uses include.mean=F but final model uses include.mean=T): A — Major, human did not raise this
- Major #8 (filtered log-likelihoods reported for simulated data, not observed data): A — Major, human did not raise this
- Major #9 (missing daily data file prevents full reproducibility): A — Major, human did not raise this
- Minor: parameter inconsistency sigma_nu = exp(4.5) in text vs exp(-4.5) in code: C — Minor, human did not raise this
- Minor: computational settings not reported in text: D — Minor, matches Human Issue #3
- Minor: no convergence traces discussed for Breto global search: C — Minor, human did not raise this
- Minor: linear correlations in global search pair plots indicate inadequate search coverage: C — Minor, human did not raise this
- Minor: tau global box upper bound spans Gaussian region (large tau indistinguishable from normal): C — Minor, human did not raise this (Human Issue #6 already covered by Major #5)
- Minor: AIC table counts IVP parameters without stating convention: C — Minor, human did not raise this
- Minor: amplitude global box lower bound is zero (unmodified model region): C — Minor, human did not raise this
- Minor: typo "parametersrs" in Section 2.4.3: C — Minor, human did not raise this
- Minor: Reference [12] is a course project, not peer-reviewed: C — Minor, human did not raise this

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1 (ESS crashes persist with t-tails): missed
- Human Issue #2 (seasonality identified but ignored in models): covered (matched by finding: "no non-mechanistic baseline; STL reveals seasonal pattern that should be captured before variance modeling")
- Human Issue #3 (computational requirements not discussed): missed
- Human Issue #4 (monthly data; volatility models usually higher-frequency): missed
- Human Issue #5 (causation language): missed
- Human Issue #6 (tau range not enforced; large tau approaches normal): covered (matched by finding: "tau and amplitude lack parameter transformation declarations")

**Findings classification:**
- Major #1 (global search uses previous mif2 result as first argument): A — Major, human did not raise this
- Major #2 (log-likelihood comparison between SV and GARCH is invalid): A — Major, human did not raise this
- Major #3 (hardcoded event windows introduce look-ahead bias): A — Major, human did not raise this
- Major #4 (initial filtered log-likelihoods reported for simulated data, not real data): A — Major, human did not raise this
- Major #5 (no profile likelihoods computed for any parameter): A — Major, human did not raise this
- Major #6 (no non-mechanistic baseline; STL reveals seasonal structure not addressed): B — Major, matches Human Issue #2
- Major #7 (tau and amplitude lack parameter transformation declarations): B — Major, matches Human Issue #6
- Major #8 (AIC table uses hardcoded log-likelihoods not extracted from live objects): A — Major, human did not raise this
- Major #9 (inadequate diagnostics: no conditional log-likelihood plot, no filtering distribution): A — Major, human did not raise this
- Major #10 (missing daily data file creates failed dependency): A — Major, human did not raise this
- Minor: sigma_nu exp sign mismatch (exp(4.5) in text vs exp(-4.5) in code): C — Minor, human did not raise this
- Minor: tau rw.sd = 1 misscaled (large perturbation, integer clamping via nearbyint): C — Minor, human did not raise this
- Minor: write.table appending in eval=FALSE chunks is vestigial code: C — Minor, human did not raise this
- Minor: GARCH AIC tie-breaking ambiguity in which.min usage: C — Minor, human did not raise this
- Minor: no seasonal decomposition of volatility time series (STL applied to log-returns, not squared returns): C — Minor, human did not raise this (Human Issue #2 already covered by Major #6)
- Minor: parameter estimates not reported in any table: C — Minor, human did not raise this
- Minor: missing daily file (duplicate mention): C — Minor, same underlying issue as Major #10

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1 (ESS crashes persist with t-tails): missed
- Human Issue #2 (seasonality identified but ignored in models): covered (matched by finding: "seasonal pattern unmodeled; STL shows seasonal component not incorporated into POMP models")
- Human Issue #3 (computational requirements not discussed): missed
- Human Issue #4 (monthly data; volatility models usually higher-frequency): missed
- Human Issue #5 (causation language): missed
- Human Issue #6 (tau range not enforced; large tau approaches normal): missed

**Findings classification:**
- 25.17.3 (hard-coded regime windows confound leverage hypothesis test): A — Major, human did not raise this
- 25.17.4 (no profile likelihoods for any model parameter): A — Major, human did not raise this
- 25.17.1 (mif2 internal log-likelihood likely used in AIC table; no replicated pfilter runs): A — Major, human did not raise this
- 25.17.6 (no mean-model baseline / ARMA/SARIMA): A — Major, human did not raise this (Human Issue #2 already covered by 25.17.14)
- 25.17.14 (seasonal pattern unmodeled; not incorporated into any POMP model): D — Minor, matches Human Issue #2
- 25.17.2 (GARCH vs. SV likelihood scale: verification of normalizing convention recommended): C — Minor, human did not raise this
- 25.17.M1 (no simulation-based POMP model diagnostics): C — Minor, human did not raise this
- 25.17.M2 (initial conditions G_0 = H_0 = 0 unjustified): C — Minor, human did not raise this

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 3 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 4 | 8 | 8 | 4 |
| B (AI major, human also found) | 1 | 1 | 2 | 0 |
| C (AI minor, human missed) | 9 | 8 | 7 | 3 |
| D (AI minor, human also found) | 1 | 1 | 0 | 1 |
| E (Human found, AI missed) | 4 | 4 | 4 | 5 |

---

## Per-Reviewer Metrics

Human Recall = (B + D) / (B + D + E)
AI-Unique Rate = (A + C) / (A + B + C + D)

| Reviewer | B | D | E | B+D | B+D+E | Human Recall | A | C | A+C | A+B+C+D | AI-Unique Rate |
|----------|--:|--:|--:|----:|------:|-------------:|--:|--:|----:|--------:|---------------:|
| Alex | 1 | 1 | 4 | 2 | 6 | 33.3% | 4 | 9 | 13 | 15 | 86.7% |
| Charlie | 1 | 1 | 4 | 2 | 6 | 33.3% | 8 | 8 | 16 | 18 | 88.9% |
| Doug | 2 | 0 | 4 | 2 | 6 | 33.3% | 8 | 7 | 15 | 17 | 88.2% |
| Evan | 0 | 1 | 5 | 1 | 6 | 16.7% | 4 | 3 | 7 | 8 | 87.5% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #1: ESS diagnostics show occasional crashes even with t-distributed tails; report notes this limitation without resolving it.
- Human Issue #3: Computational requirements of the experiments are not discussed.
- Human Issue #4: The project uses monthly data, whereas volatility models are most commonly developed and used for higher-frequency data.
- Human Issue #5: The language may imply causation (e.g., government policies causing leverage effects) without sufficient evidence.

Count: 4 out of 6 human issues (66.7%) were missed by all four reviewers.

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #6 (tau range not enforced / large tau approaches normal): covered by Alex, Charlie, and Doug — not a unique find for any single reviewer.
- Human Issue #2 (seasonality identified but ignored): covered by Alex, Doug, and Evan — not a unique find for any single reviewer.

No human issue was covered by exactly one reviewer.

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |

### Universal AI-only flags

Issues raised by every reviewer that the human did not mention:

Reviewing findings across all four reviewers for unanimous AI-only flags:

- Hard-coded regime windows / look-ahead bias / data snooping: raised by Alex (Major #1), Charlie (Major #2), Doug (Major #3), Evan (Major 25.17.3) — all four reviewers, human did not raise this.
- No profile likelihoods: raised by Alex (not explicitly — Alex mentions AIC penalty discussion; actually Alex does not have a standalone "no profile likelihood" finding), Charlie (Major #3), Doug (Major #5), Evan (Major 25.17.4). Alex's finding #8 mentions the AIC difference of 1.4 units but does not explicitly call for profile likelihoods. This is not unanimous across all four.
- Missing daily data file: raised by Alex (Major #2), Charlie (Major #9), Doug (Major #10) — but not by Evan. Not unanimous.
- Filtered log-likelihoods on simulated data: raised by Alex (Major #13 — but classified as Minor in Alex), Charlie (Major #8), Doug (Major #4) — but not by Evan. Not unanimous.

Checking more carefully for universal flags:

Hard-coded regime windows: Alex Major #1, Charlie Major #2, Doug Major #3, Evan Major 25.17.3 — all four. Human did not raise this. **Universal AI-only flag.**

No profile likelihoods: Charlie Major #3, Doug Major #5, Evan Major 25.17.4 — three of four (Alex has related finding #8 about AIC difference not being decisive, but does not explicitly call for profile likelihoods). Not unanimous.

Global search anti-pattern (mif2 initialized from previous mif2 result): Charlie Major #1, Doug Major #1 — only two of four. Not unanimous.

**Universal AI-only flags (raised by all four reviewers, human did not mention):**

1. Hard-coded regime windows (specific time indices for 2008 recession and 2020 pandemic) constitute data snooping / look-ahead bias and confound the main leverage hypothesis test.

Count: 1 universal AI-only flag.
