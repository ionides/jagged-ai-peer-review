# Comparator Analysis — W21 Project 07

---

## Human Issues

1. "Profile is flat, suggesting convergence issues or nonlinearity of the likelihood surface". Neither of these is necessary for a flat profile. There can be a linear tradeoff between parameters, and perfect convergence, and a flat profile will result. An appropriate conclusion could be weak identifiability, or non-identifiability for a perfectly flat profile.

2. It may be unsurprising that simulations do not agree with the particular timing of the information epidemic peaks - the model has no information to let it do this. We can just look for descriptive properties such as peak size and width, which seem like a reasonable match.

3. Rather than estimating $N$ to fit in with the normalization, one could perhaps try to include the normalization in the measurement model? It is not immediately clear how to do that, so it would need more work.

4. The plots called "profiles" are incorrectly calculated. From the code, we see they are computed as a profile over $\eta$ and plotted against other parameters. That may explain some of the issues with interpreting the plots.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "Profile code uses `guesses` instead of `guesses2` — profiles are not profile likelihoods"; also matched by finding: "Profile CI for Beta extracted from global search scatter, not a proper profile")

**Findings classification:**
- Finding 1 (Global Search at run_level=1): A — global search run at debug-level settings yields unreliable inference
- Finding 2 (Profile code guesses vs guesses2): B — profile code iterates over `guesses` instead of `guesses2`; results are a second global search, not a profile likelihood (matches Human Issue #4)
- Finding 3 (Negative Binomial mis-parameterized): A — `dnbinom` called with H as size and rho as prob, producing wrong mean
- Finding 4 (mif2 missing Nmif label): A — `Nmif` passed positionally without argument name, likely silent bug
- Finding 5 (Profile CI from global search): B — CI for Beta extracted from global search scatter by min/max, not from a proper profile likelihood (matches Human Issue #4)
- Finding 6 (Data preprocessing "<1" replaced with 0): A — interval-censored observations treated as exact zeros without justification
- Finding 7 (rw.sd omits key parameters): C — `rw.sd` in second search only perturbs Beta and rho, leaving other parameters frozen
- Finding 8 (No likelihood ratio test): C — no formal comparison against a simpler null model
- Finding 9 (N unidentifiable): C — N and rho confounded; N interpretation unclear given normalized data
- Finding 10 (Spectral analysis on second half only): C — periodogram computed on post-spike data only, introducing selection bias
- Finding 11 (Initial conditions partially fixed): C — I(0)=5 is hard-coded without sensitivity analysis
- Finding 12 (H accumulator initialized to 5): C — H initialized to non-zero value; arbitrary and undocumented
- Finding 13 (Pairs plot mixes guesses and results): C — overlaying raw guesses on likelihood scatter adds visual noise
- Finding 14 (Conclusion overstates evidence): C — conclusion too optimistic given inconclusive parameter search and weak simulation agreement
- Finding 15 (No convergence diagnostics): C — no MIF2 trace plots to assess whether optimization converged

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "Data normalization makes count-based measurement model questionable")
- Human Issue #4: covered (matched by finding: "Profile likelihood iterates over wrong design — results2 never uses guesses2")

**Findings classification:**
- Finding 1 (Profile likelihood iterates over wrong design): B — profile computation iterates over wrong grid, producing scatterplot not true profile likelihoods (matches Human Issue #4)
- Finding 2 (Final analysis runs at debug-level computation): A — run_level=1 with Np=100, Nmif=10 invalidates all results
- Finding 3 (Measurement model formally misspecified — H as size parameter): A — H used as NegBin size/dispersion parameter instead of mean parameter
- Finding 4 (Key parameters rho and N not perturbed in mif2): A — rho and N excluded from rw.sd so never optimized
- Finding 5 (No convergence diagnostics shown): A — no mif2 trace plots anywhere in the report
- Finding 6 (No benchmark comparison): A — no non-mechanistic model comparison provided
- Finding 7 (Arbitrary hard filter on loglik removes valid results): A — filter discards best-fitting runs without justification
- Finding 8 (Data normalization makes count-based measurement model questionable): B — Google Trends indices are not counts; NegBin measurement model and rho/N interpretation break down (matches Human Issue #3)
- Finding 9 (Profile eta range too narrow): C — profile range [0.01, 0.1] may miss MLE given global search upper bound of 1.0
- Finding 10 (Profile for mu_RS uninformative but no structural response): C — non-identifiability of mu_RS warrants SIR vs. SIRS model comparison, not just acknowledgment
- Finding 11 (Simulation diagnostics are forward simulations, not filtering-distribution simulations): C — forward simulations do not condition on data and cannot diagnose model failure
- Finding 12 (loglik.se threshold too permissive): C — loglik.se < 2 is very large, likely reflecting Np=100
- Finding 13 (Profile mif2 cooling fraction differs from global search): C — cooling.fraction.50=0.3 in profile vs. 0.5 in global search unexplained
- Finding 14 (Commented-out code left in Rmd): C — abandoned analysis paths not explained or removed
- Finding 15 ("Benchmark" refers to manually chosen parameter set): C — manually chosen parameter set is not a benchmark in the standard sense

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "Population N treated as a free parameter on normalized data — a more principled approach would model normalization in the measurement model")
- Human Issue #4: covered (matched by finding: "Pseudo-profile likelihood: no dedicated profile IF2 search was ever executed — profiles are scatter plots from global search, not constrained optimizations")

**Findings classification:**
- Finding 1 (pseudo-profile likelihood): B — profile plots are not genuine profile likelihoods; they are scatter plots from the global search with no constrained optimization (matches Human Issue #4)
- Finding 2 (no non-mechanistic benchmark): A — SIRS model never compared against any non-mechanistic baseline
- Finding 3 (run_level=1 inadequate computation): A — analysis run at debugging level with Np=100, Nmif=10
- Finding 4 (misspecified negative binomial): A — dmeasure uses H as size parameter and rho as probability, not the standard dnbinom_mu parameterization
- Finding 5 (rho excluded from rw.sd): A — rho and N frozen at random starting points during IF2 without justification
- Finding 6 (H=5 initial condition not reset): A — H initialized to 5 but accumvars mechanism resets to 0 after each observation, creating inconsistency at t=0
- Finding 7 (N as free parameter on normalized data): B — N estimated from data normalized to max 100, making N and rho uninterpretable; suggests modeling normalization in measurement model (matches Human Issue #3)
- Finding 8 (benchmark at manual params, not MLE): C — pre-search log-likelihood evaluated at hand-chosen simulation parameters
- Finding 9 (eta profile never plotted): C — profile_design constructs grid over eta but no eta profile appears in Section 5.2
- Finding 10 (Nmif argument passed incorrectly): C — Nmif passed positionally without naming it in mif2() call
- Finding 11 (goodness-of-fit purely visual): C — no AIC, no log-likelihood ratio test, no conditional log-likelihood plot
- Finding 12 (H accumulates dN_SI vs. search frequency): C — relationship between new infections accumulator and search frequency not discussed
- Finding 13 (no convergence diagnostics): C — no trace plots or pairs plots; especially problematic given run_level=1
- Finding 14 (no model corroboration with external knowledge): C — parameter estimates not compared to epidemiological or social-media literature
- Finding 15 (notation inconsistency beta vs. Beta): C — mathematical section uses lowercase β but code and results use Beta

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "21.07.M3 — population size N has no clear physical interpretation given the normalized Google Trends data")
- Human Issue #4: covered (matched by finding: "21.07.2 — profile likelihood computation iterates over the wrong grid, making the profile plots invalid")

**Findings classification:**
- 21.07.1: A — debug-scale computations throughout (run_level=1)
- 21.07.2: B — profile likelihood computation uses the wrong grid, invalidating all profile plots and CIs (matches Human Issue #4)
- 21.07.3: A — no benchmark comparison against non-mechanistic model
- 21.07.4: A — no convergence diagnostics (no IF2 trace plots)
- 21.07.5: C — measurement model passes H (accumulator) as the negative binomial size/dispersion parameter
- 21.07.6: C — rho and N excluded from rw.sd despite being listed as variable parameters
- 21.07.7: C — spectral analysis subsets to last 43 days without justification
- 21.07.M1: C — ESS not monitored during particle filtering
- 21.07.M2: C — best log-likelihood not stated in narrative prose
- 21.07.M3: D — population size N has no clear physical interpretation given normalized Google Trends data (matches Human Issue #3)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 4 | 6 | 5 | 3 |
| B (AI major, human also found) | 2 | 2 | 2 | 1 |
| C (AI minor, human missed) | 9 | 7 | 8 | 5 |
| D (AI minor, human also found) | 0 | 0 | 0 | 1 |
| E (Human found, AI missed) | 3 | 2 | 2 | 2 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 2 | 0 | 3 | 1/4 = 25% | 4 | 9 | 13/15 = 87% |
| Charlie | 2 | 0 | 2 | 2/4 = 50% | 6 | 7 | 13/15 = 87% |
| Doug | 2 | 0 | 2 | 2/4 = 50% | 5 | 8 | 13/15 = 87% |
| Evan | 1 | 1 | 2 | 2/4 = 50% | 3 | 5 | 8/10 = 80% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #1: "Profile is flat, suggesting convergence issues or nonlinearity of the likelihood surface". Neither of these is necessary for a flat profile. There can be a linear tradeoff between parameters, and perfect convergence, and a flat profile will result. An appropriate conclusion could be weak identifiability, or non-identifiability for a perfectly flat profile. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #2: It may be unsurprising that simulations do not agree with the particular timing of the information epidemic peaks - the model has no information to let it do this. We can just look for descriptive properties such as peak size and width, which seem like a reasonable match. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 2 out of 4 human issues (50%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

(none)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |
