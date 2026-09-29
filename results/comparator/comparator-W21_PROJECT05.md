# Comparator Analysis — W21 Project 05

---

## Human Issues

1. There is evidence of model misspecification. The perturbed model (with parameters having a random walk) obtains log likelihoods around -300. As the perturbations decrease, the likelihood goes down and filtering failures (large drops in the estimated likelihood) start occurring. This is most likely a result of insufficient process and/or measurement noise.

2. All models use binomial measurement, which can be problematic partly because of the bounded support and partly because it cannot fit overdispersion. Similarly, no models included additional noise in the rates.

3. The model is not fully described (via mathematical equations). The parameter eta is not defined, except by the computer code.

4. Initializing to $I=1$ seems a strong assumption, but works out okay here.

5. Reference list is limited to course notes, plus the data set source. More context could be added.

6. The likelihood at the initial guess is not scientifically as important as the likelihood after parameter estimation - better to report the latter instead.

---

## Alex

**Coverage record:**
- Human Issue #1: covered (matched by finding: "NaN Log-Likelihoods Accepted Without Diagnosis" — both address filtering failures indicating model problems)
- Human Issue #2: covered (matched by finding: "No Overdispersion in Measurement Model Despite Clear Evidence of Need" — directly matches binomial measurement/overdispersion concern)
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "References Section Is Minimal" — identifies same two references: CDC data and course notes)
- Human Issue #6: missed

**Findings classification:**
- Finding 1 (No Global Search): A — no global search; analysis terminates after single local search
- Finding 2 (Code Bug SIR2 Likelihood): A — SIR2 likelihood block prints first model's likelihood instead of third model's
- Finding 3 (Hard-Coded Contact-Rate Reduction): A — 0.7 multiplier is fixed, not estimated from data
- Finding 4 (Measurement Model H Accumulates Without Reset): A — H conflates cumulative recoveries with reported incidence
- Finding 5 (No Overdispersion in Measurement Model): B — all models use binomial measurement despite need for overdispersion (matches Human Issue #2)
- Finding 6 (NaN Log-Likelihoods Accepted Without Diagnosis): B — filtering failures/NaN likelihoods not investigated (matches Human Issue #1)
- Finding 7 (Only One Flu Season Modeled): A — single season fitted despite multi-season data and research question
- Finding 8 (Unstable Local Search, Low Np): C — Nmif=50 and Np=2000 likely insufficient for convergence
- Finding 9 (Likelihood Comparison Informal): C — no formal AIC or likelihood ratio test applied
- Finding 10 (Conclusion Contradicts Likelihood Evidence): C — best log-likelihood is SIR2 but conclusion names SEIR as better fit
- Finding 11 (Raw Counts vs. Percent Positive): C — raw positive counts conflate incidence with testing intensity
- Finding 12 (No Sensitivity Analysis for Fixed Parameters): C — fixed N and 0.7 multiplier never subjected to sensitivity checks
- Finding 13 (mu_EI Implausible Values): C — SEIR latency rate implies <1-day latent period, not discussed
- Finding 14 (Figure Captions Incorrect Date Ranges): C — figure caption date range inconsistent with modeling scope
- Finding 15 (References Section Minimal): D — only CDC data and course notes cited (matches Human Issue #5)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Major-5: Extreme Monte Carlo Standard Errors Invalidate Model Comparisons — particle filter degeneracy / filtering failures as symptom of model misspecification")
- Human Issue #2: covered (matched by finding: "Minor-binomial: Binomial measurement model without overdispersion")
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed

**Findings classification:**
- Major-1 (Code Bug: Model 3 Likelihood Printed Incorrectly): A — code bug causes wrong model's likelihood to print, driving false conclusion that all models fail
- Major-2 (Measurement Model Observes Recoveries Instead of New Infections): A — H accumulates dN_IR rather than dN_SI; fundamental measurement model misspecification
- Major-3 (Contact Rate Reduction Factor Hardcoded): A — 0.7 multiplier in Model 3 is a fixed constant rather than an estimated parameter
- Major-4 (No Global Search): A — all 20 mif2 runs start from the same single initial point; no convergence evidence
- Major-5 (Extreme Monte Carlo Standard Errors): B — SE up to 95 loglik units indicates particle filter degeneracy / filtering failures, symptom of model misspecification (matches Human Issue #1)
- Major-6 (No Non-Mechanistic Benchmark Comparison): A — no ARMA/ARIMA baseline fitted
- Major-7 (No Profile Likelihoods): A — no profile likelihoods computed, parameter identifiability unassessed
- Major-8 (Conclusion Contradicts Saved Likelihood Evidence): A — conclusion that all models fail contradicts sir2_lik.csv showing Model 3 loglik of -333.4 (SE=1.37)
- Minor-nmif (Nmif=50 below course standard): C — local search uses 50 iterations rather than the run_level=2 standard of 100
- Minor-nots (No classical time series analysis): C — no ARIMA baseline section
- Minor-bioplaus (Biological plausibility of parameters not discussed): C — mu_IR values implying 0.5–4.7 day infectious periods and implausibly high R0 not evaluated
- Minor-eta (eta = 0.0853 implies only 8.5% susceptible): C — biological plausibility of near-9-million immune population at season start not discussed
- Minor-binomial (Binomial measurement model without overdispersion): D — binomial dmeas used throughout; negative binomial or beta-binomial would be more appropriate given TOTAL.SPECIMENS variability (matches Human Issue #2)
- Minor-loglik (logLik() called on list): C — non-standard use of logLik() dispatch on list; sapply pattern would be clearer
- Minor-weekindex (Week index instead of calendar dates): C — integer 1–52 time variable makes interpretation of "week 22" ambiguous without cross-referencing data setup
- Minor-typos (Typos in text): C — multiple spelling errors including "contatct", "simualte", "wihch", "casese"
- Minor-seir (SEIR conclusion mismatch): C — text notes lowest loglik of -860.9967 but visual simulation misfit is noted without further investigation
- Minor-season19 (No description of season19 construction in SEIR section): C — fluSEIR rebuilt redundantly from df inside SEIR chunk rather than referencing existing object

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Binomial measurement model causes structural particle filter collapse — bounded support causes -Inf likelihoods, the same symptom the human attributes to insufficient measurement noise")
- Human Issue #2: covered (matched by finding: "Binomial measurement model causes structural particle filter collapse — directly identifies bounded support and absence of overdispersion as the structural problem")
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed

**Findings classification:**
- Finding 1 (Accumulator H tracks recoveries not infections): A — fundamental measurement model mismatch, accumulator bug not identified by human
- Finding 2 (Third model displays wrong likelihood — SIR1 value shown for SIR2): A — copy-paste display error not identified by human
- Finding 3 (Binomial measurement model causes structural particle filter collapse): B — matches Human Issues #1 and #2
- Finding 4 (No global search — convergence conclusions premature): A — missing global search not identified by human
- Finding 5 (Hardcoded 0.7 contact-rate reduction factor not estimated): A — fixed reduction factor not identified by human
- Finding 6 (No non-mechanistic benchmark comparison): A — missing ARIMA baseline not identified by human
- Finding 7 (No profile likelihoods or confidence intervals): A — missing profiles not identified by human
- Finding 8 (Large log-likelihood standard errors indicate particle filter degeneracy): A — large pfilter SEs not identified by human
- Finding 9 (Log-likelihood direction inverted in SEIR conclusion): C — "lowest loglikelihood" phrasing error not identified by human
- Finding 10 (SEIR pomp object inherits incomplete partrans from fluSIR): C — partrans inheritance bug not identified by human
- Finding 11 (Population N fixed without biological justification): C — N justification issue not identified by human
- Finding 12 (Week-22 COVID-19 breakpoint chosen by inspection): C — breakpoint justification not identified by human
- Finding 13 (No model diagnostics beyond visual simulation overlay): C — missing diagnostics not identified by human
- Finding 14 (Only 50 IF2 iterations with Np=2000 — computational effort not assessed): C — computational adequacy issue not identified by human
- Finding 15 (Research question mismatches analysis performed): C — research question mismatch not identified by human

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "21.05.M6 — binomial measurement imposes insufficient variance; cannot capture overdispersion; negative-binomial preferred but not implemented")
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "21.05.m5 — references vague and incomplete; dataset lacks URL and access date; lecture notes lack chapter/year")
- Human Issue #6: missed

**Findings classification:**
- 21.05.M1: A — no non-mechanistic benchmark comparison; POMP log-likelihoods uninterpretable without baseline
- 21.05.M2: A — no global search; convergence not demonstrated; trace plots show parameters bouncing without settling
- 21.05.M3: A — 0.7 contact-rate multiplier in Model 3 hard-coded rather than estimated, failing to answer the stated research question
- 21.05.M4: A — wrong likelihood object printed for Model 3 (prints sir_L_pf instead of sir2_L_pf), reporting Model 1's value
- 21.05.M5: A — no profile likelihoods or confidence intervals for any parameter
- 21.05.M6: B — binomial measurement forces insufficient variance, underfits overdispersion in weekly counts (matches Human Issue #2)
- 21.05.m1: C — sign convention confusion; manuscript says "lowest loglikelihood" when meaning best (least negative) value
- 21.05.m2: C — NaN log-likelihoods attributed to model misspecification rather than particle degeneracy/collapse
- 21.05.m3: C — no software version information or sessionInfo() output
- 21.05.m4: C — deprecated R idioms (funs(), guides(color=FALSE)) that will generate warnings
- 21.05.m5: D — references vague and incomplete; missing URLs, access dates, and chapter specifics (matches Human Issue #5)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 5 | 7 | 7 | 5 |
| B (AI major, human also found) | 2 | 1 | 1 | 1 |
| C (AI minor, human missed) | 7 | 9 | 7 | 4 |
| D (AI minor, human also found) | 1 | 1 | 0 | 1 |
| E (Human found, AI missed) | 3 | 4 | 4 | 4 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 2 | 1 | 3 | 3/6 = 50% | 5 | 7 | 12/15 = 80% |
| Charlie | 1 | 1 | 4 | 2/6 = 33% | 7 | 9 | 16/18 = 89% |
| Doug | 1 | 0 | 4 | 2/6 = 33% | 7 | 7 | 14/15 = 93% |
| Evan | 1 | 1 | 4 | 2/6 = 33% | 5 | 4 | 9/11 = 82% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #3: The model is not fully described (via mathematical equations). The parameter eta is not defined, except by the computer code. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #4: Initializing to $I=1$ seems a strong assumption, but works out okay here. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #6: The likelihood at the initial guess is not scientifically as important as the likelihood after parameter estimation - better to report the latter instead. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 3 out of 6 human issues (50%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

(none)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |
