# Comparator Analysis — W22 Project 05

---

## Human Issues

1. Weekly periodicity cannot be described by GARCH.

2. Heteroskedasticity does not explain dependence. They are different things: heteroskedasticity is about variances, and dependence may be explained by covariances.

3. An ARMA-GARCH model is attempted to show how extended approaches to address heteroscedasticity are not sufficient to overcome the problem. This is an interesting idea, though it will not address the periodicity. It would be good to write out the model for an ARMA-GARCH model, so that readers do not have to track down the given reference.

4. Very few replications are carried out for the Monte Carlo inference. This may be due to time constraints, but such limitations need to be mentioned.

5. Avoid raw, unprocessed R output.

6. Why is the pairs plot so sparse? Is it because a likelihood cutoff was used which led to only one point being included? A referee noticed that, in the plots of local search, the reader can find that log likelihood doesn't converge in the process of iteration. By looking into the code, we find that the iterating filter was done for 20 times, but only 8 of them are shown on the plot, which means the other 12 of them got problematic results. The common case is that the functions of `rmeasure` and `dmeasure` aren't set properly so they return `NA` values, or the model design needs to be improved. In practice, some bad initial values of parameters can also cause this problem. The authors can try to solve this problem by tuning the parameters, debugging the measurement functions or redesigning the model.

7. It would be interesting to see a likelihood comparison between the different models.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by findings: "IF2 local search uses only 8 chains — severely underpowered Monte Carlo" and "pairs plots show only 8 local search points — effectively uninformative")
- Human Issue #5: missed
- Human Issue #6: covered (matched by findings: "critical bug in dmeasure condition — always-true guard", "inconsistency between dmeasure and rmeasure standard deviation formulas", and "pairs plots show only 8 local search points — effectively uninformative")
- Human Issue #7: missed

**Findings classification:**
- Finding 1: A — primary research question (counterfactual vaccination scenarios) never answered
- Finding 2: B — critical bug in dmeasure condition makes guard always true, dmeasure/rmeasure not set properly (matches Human Issue #6)
- Finding 3: B — dmeasure and rmeasure use different sd formulas, inconsistency between generative and evaluation models (matches Human Issue #6)
- Finding 4: A — model equations have errors: V compartment absorbing, N_VE flow missing from E equation
- Finding 5: B — IF2 local search hard-codes only 8 chains, severely underpowered Monte Carlo inference (matches Human Issue #4)
- Finding 6: A — model does not use actual vaccination data as covariate despite availability
- Finding 7: A — no profile likelihood or confidence intervals for any parameters
- Finding 8: A — ARMA-GARCH section not executed (eval=F), no results shown at all
- Finding 9: C — beta_t piecewise definition has garbled typographical errors and label inconsistencies
- Finding 10: C — S(0) initial condition equation is self-referential
- Finding 11: C — initial_R computed from only 6 months of prior cases, understating true recovered population
- Finding 12: D — pairs plots show only 8 local search points, too sparse to characterize likelihood surface (matches Human Issues #4 and #6)
- Finding 13: C — loglik.se < 0.5 filter criterion is nonstandard and unjustified
- Finding 14: C — ARIMA section conflates first difference of daily cases with model of daily cases
- Finding 15: C — missing model diagram image due to case-sensitive filename mismatch

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "Critically insufficient computation — replicate(5) yields very noisy likelihood estimates")
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "Defective dmeasure condition renders likelihood evaluation unreliable"; also matched by "Critically insufficient computation — replicate(5) yields very noisy likelihood estimates"; also matched by "No convergence demonstrated for iterated filtering"; also matched by "Pairs plot used as substitute for profile likelihood without acknowledgement")
- Human Issue #7: covered (matched by finding: "No benchmark comparison — no log-likelihood comparison between POMP and ARIMA")

**Findings classification:**
- Finding 1 (Defective dmeasure condition): B — dmeasure OR guard is trivially true, invalidating all likelihoods (matches Human Issue #6)
- Finding 2 (Critically insufficient computation): B — replicate(5) and low particle counts yield unreliable likelihoods (matches Human Issues #4 and #6)
- Finding 3 (No convergence demonstrated): B — log-likelihood ranges -7000 to -5000 with no upward trend (matches Human Issue #6)
- Finding 4 (No profile likelihoods): A — no profile likelihoods or confidence intervals computed for any parameter
- Finding 5 (No benchmark comparison): B — no log-likelihood comparison against IID or ARIMA baseline (matches Human Issue #7)
- Finding 6 (Stated scientific goal never executed): A — counterfactual vaccine scenario analysis is never performed
- Finding 7 (Vaccinated compartment dynamics inconsistent): A — mathematical exposition adds N_SV to Exposed compartment, contradicting code
- Finding 8 (Local search uses mif2 loglik directly): A — best run selected from unreliable mif2 internal loglik before re-evaluation
- Finding 9 (Measurement model not epidemiologically justified): A — Gaussian model for count data not justified; no comparison to negative binomial
- Finding 10 (Global search box includes fixed parameters): A — single-value rows in covid_box create fragile implicit structure
- Finding 11 (rw.sd values halved without justification): C — perturbation size 0.01 rather than course standard 0.02
- Finding 12 (S(0) circular reference): C — initialization equation is self-referential in write-up though code is correct
- Finding 13 (No model diagnostics): C — no conditional log-likelihoods, ESS, or filtering distributions examined
- Finding 14 (Pairs plot as substitute for profile likelihood): D — sparse pairs plot treated as characterizing identifiability without profile analysis (matches Human Issue #6)
- Finding 15 (Spelling and grammatical errors): C — recurring misspellings and inconsistent beta notation throughout

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 4 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: covered (matched by finding: "ARIMA model selection ignores weekly seasonality")
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "Computational effort is grossly inadequate — only 8 local-search replicates, insufficient particles")
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "IF2 convergence failure acknowledged but results presented regardless"; also matched by "dmeasure uses poorly specified Gaussian with asymmetric condition"; also matched by "dmeasure and rmeasure use inconsistent normal parameterizations")
- Human Issue #7: covered (matched by finding: "Complete absence of benchmark comparison — no log-likelihood/AIC comparison between ARIMA and POMP")

**Findings classification:**
- Finding 1 (complete absence of benchmark comparison): B — no log-likelihood or AIC comparison between ARIMA and POMP models (matches Human Issue #7)
- Finding 2 (IF2 convergence failure acknowledged, results presented regardless): B — convergence failure is the core of the pairs-plot/iteration problem (matches Human Issue #6)
- Finding 3 (computational effort grossly inadequate, reporting incomplete): B — only 8 local-search replicates, insufficient particles, no stated limitations (matches Human Issue #4)
- Finding 4 (no profile likelihood or confidence intervals): A — identifiability analysis entirely absent; human did not raise this
- Finding 5 (primary research question never answered): A — simulation study is completely absent; human did not raise this
- Finding 6 (dmeasure uses poorly specified Gaussian with asymmetric dead-code condition): B — faulty dmeasure specification is the rmeasure/dmeasure NA-producing issue flagged by the human (matches Human Issue #6)
- Finding 7 (dmeasure and rmeasure use inconsistent normal parameterizations): B — rmeasure/dmeasure inconsistency directly matches the human's concern about measurement functions returning bad values (matches Human Issue #6)
- Finding 8 (global search uses run-level-dependent particle counts with no reported level): A — undisclosed computational configuration; human did not raise this
- Finding 9 (global search initialization: several parameters not randomized across replicates): A — parameter-box audit finding; human did not raise this
- Finding 10 (no model diagnostics beyond convergence traces): A — absence of conditional log-likelihood and ESS plots; human did not raise this
- Finding 11 (compartment model likely typo in E(t) equation): C — N_SV vs. N_VE transcription error in writeup
- Finding 12 (S(0) definition is circular): C — S(0) appears on both sides of its own equation
- Finding 13 (ARIMA model selection ignores weekly seasonality): D — same underlying concern as human's point that weekly periodicity is not handled by the baseline time-series models (matches Human Issue #1)
- Finding 14 (ARMA-GARCH failure treated as evidence of model inadequacy without diagnostic investigation): C — concerns the undisclosed cause of Hessian non-invertibility, not the inability to handle periodicity or missing model equations
- Finding 15 (references formatted inconsistently and contain unprofessional citations of student projects): C — citation quality issue; human did not raise this

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 5 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by findings: "22.05.5 — Monte Carlo noise in log-likelihood not addressed" and "22.05.15 — Computational parameters not reported")
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "22.05.6 — No profile likelihoods or parameter confidence intervals; pairs plots sparse")
- Human Issue #7: covered (matched by finding: "22.05.7 — No benchmark comparison between POMP and non-mechanistic models")

**Findings classification:**
- 22.05.8: A — stated scientific goal (counterfactual simulation) not achieved
- 22.05.7: B — no benchmark log-likelihood comparison between POMP and non-mechanistic models (matches Human Issue #7)
- 22.05.2/22.05.3: A — structural errors in compartment equations (V(t) balance and self-referential S(0))
- 22.05.6: B — no profile likelihoods; pairs plot sparse, confirming unreliable inference (matches Human Issue #6)
- 22.05.5: B — Monte Carlo log-likelihood noise (loglik.se > 0.2) not addressed; too few replicates (matches Human Issue #4)
- 22.05.1: A — global search substantially underperforms local search without explanation
- 22.05.15: D — computational parameters (Np, Nmif, replicates) not reported (matches Human Issue #4)
- 22.05.16: C — non-standard truncated normal measurement model for count data
- 22.05.4: C — AIC table non-monotonicity for higher-order ARIMA not discussed
- 22.05.9: C — piecewise beta notation uses inconsistent inequality signs at boundaries
- Notation/typos: C — multiple manuscript typos and absent figure captions

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 5 | 6 | 5 | 3 |
| B (AI major, human also found) | 3 | 4 | 5 | 3 |
| C (AI minor, human missed) | 6 | 4 | 4 | 4 |
| D (AI minor, human also found) | 1 | 1 | 1 | 1 |
| E (Human found, AI missed) | 5 | 4 | 3 | 4 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 3 | 1 | 5 | 2/7 = 29% | 5 | 6 | 11/15 = 73% |
| Charlie | 4 | 1 | 4 | 3/7 = 43% | 6 | 4 | 10/15 = 67% |
| Doug | 5 | 1 | 3 | 4/7 = 57% | 5 | 4 | 9/15 = 60% |
| Evan | 3 | 1 | 4 | 3/7 = 43% | 3 | 4 | 7/11 = 64% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #2: Heteroskedasticity does not explain dependence. They are different things: heteroskedasticity is about variances, and dependence may be explained by covariances. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #3: An ARMA-GARCH model is attempted to show how extended approaches to address heteroscedasticity are not sufficient to overcome the problem. This is an interesting idea, though it will not address the periodicity. It would be good to write out the model for an ARMA-GARCH model, so that readers do not have to track down the given reference. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #5: Avoid raw, unprocessed R output. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 3 out of 7 human issues (43%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #1: Weekly periodicity cannot be described by GARCH. (Covered only by Doug)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 1 |
| Evan | 0 |
