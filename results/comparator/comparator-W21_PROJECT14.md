# Comparator Analysis — W21 Project 14

---

## Human Issues

1. The project interprets the maximization difficulty in terms of the challenge of searching a large box. The local search is quite successful, with many searches jumping up to the consensus maximum around 500. The global search finds two modes, one with a reporting rate around 10% and another with a close to 100%. The latter corresponds to quite a different interpretation, where depletion of susceptibles has no dynamic importance. There is also some hint of a third mode, with even lower reporting rate.

2. The log likelihood search sometimes falls off a likelihood cliff, perhaps because the binomial distribution in the measurement and/or process models does not always have quite enough stochasticity to explain the data. Viewing the log likelihood on this scale makes it hard to distinguish the likelihoods of the candidate modes.

3. The measurement model in the code is negative binomial, rather than the binomial reported in the text, so if overdispersion is the issue it could be needed in the process model.

4. A section on potential future work can be useful, particularly given the restrictive time limitations of a course final project.

5. The search and results might look cleaner if phase were reparameterized to take values only in $(0,2\pi)$ since otherwise the periodicity of phase adds extra clutter to the numerical results.

---

## Alex

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Convergence Diagnostics Are Incomplete for Global Search — multimodality in rho, log-likelihood cliff, no comparison of modes")
- Human Issue #2: covered (matched by finding: "Measurement Model Misspecification: Negative Binomial Uses H Incorrectly — degenerate distribution when H small, causing -Inf likelihoods / cliff"; also matched by finding: "Convergence Diagnostics Are Incomplete for Global Search — log-likelihood cliff shape, difficulty distinguishing candidate modes")
- Human Issue #3: covered (matched by finding: "The Report Describes the Measurement Model as 'Binomial' in the Text But Implements Negative Binomial")
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "Parameter Transformation Is Incomplete — Phi (phase) is meaningful only modulo 2pi, should be constrained")

**Findings classification:**
- Finding 1 [Major] — Measurement Model Misspecification: Negative Binomial Uses H Incorrectly: B — H used as size parameter in dnbinom causing degenerate likelihood, explaining the cliff (matches Human Issue #2)
- Finding 2 [Major] — H Is Used as Both Accumulator and Distribution Parameter, R(t) Never Tracked: A
- Finding 3 [Major] — Initial Conditions for E and I Are Hard-Coded and Not Estimated: A
- Finding 4 [Major] — Global Search Reuses a Single mifs_local[[1]] Chain Rather Than Fresh mif2 Calls: A
- Finding 5 [Major] — Profile Likelihood for Rho Does Not Fix Rho During Optimization: A
- Finding 6 [Major] — mu_EI and mu_IR Are Fixed Without Justification of Rate Units: A
- Finding 7 [Moderate] — Only a Single Simulation Is Shown for Local and Global Fit Assessment: C
- Finding 8 [Moderate] — Convergence Diagnostics Are Incomplete for Global Search: D — log-likelihood cliff, multimodality in rho, no comparison of candidate modes (matches Human Issues #1 and #2)
- Finding 9 [Moderate] — Parameter Transformation Is Incomplete — b1, b2, Phi Unconstrained: D — Phi meaningful only modulo 2pi, phase should be constrained to (0, 2pi) (matches Human Issue #5)
- Finding 10 [Moderate] — Profile Likelihood CI Uses Observed Min/Max Rather Than Wilks Inversion on Smooth Curve: C
- Finding 11 [Moderate] — No Baseline Model Comparison: C
- Finding 12 [Moderate] — Text Describes Measurement Model as Binomial But Code Implements Negative Binomial: D — direct text/code mismatch on measurement model (matches Human Issue #3)
- Finding 13 [Minor] — run_level = 2 Hard-Coded, SE Adequacy Not Commented On: C
- Finding 14 [Minor] — Figure Numbering Gap (Figure 10 Appears Before Figure 9 in Output): C
- Finding 15 [Minor] — Pairwise Plots Based on Only 10 Points (head(10)): C

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 3 |
| E (Human found, AI missed) | 1 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "Incorrect Negative Binomial Parameterization in Measurement Model — code uses NB rather than binomial reported in text, with incorrect parameterization")
- Human Issue #4: missed
- Human Issue #5: missed

**Findings classification:**
- Finding 1 (Incorrect Negative Binomial Parameterization): B — code uses negative binomial rather than the binomial described in text, with wrong parameterization making rho uninterpretable (matches Human Issue #3)
- Finding 2 (No Benchmark Comparison): A — SEIR POMP model never compared against any non-mechanistic benchmark
- Finding 3 (Goodness-of-Fit Assessed Only by Single-Run Visual Simulation): A — single stochastic realization insufficient for model adequacy assessment
- Finding 4 (Fixed Parameters Without Sensitivity Analysis): A — mu_EI and mu_IR fixed without sensitivity analysis, artificially narrowing profile CI
- Finding 5 (Profile Likelihood Only for One Parameter): A — profile likelihoods computed only for rho despite ridge-like correlations suggesting other parameters may be non-identifiable
- Finding 6 (Global Search Initialized from Only a Single Local Search Result): A — all 60 global replicates inherit mif2 settings from first local search result only
- Finding 7 (No Model Diagnostics): C — ESS and conditional log-likelihood plots not presented
- Finding 8 (R Compartment Not Tracked): C — recovered compartment absent from state vector; population conservation unverified
- Finding 9 (Conclusion Overstates Model Adequacy): C — conclusion claims good fit without benchmark or formal goodness-of-fit statistic
- Finding 10 (Slow/Incomplete Convergence for Eta in Global Search): C — eta does not converge to consistent value across global search trajectories
- Finding 11 (Global Search Box Too Wide for b1 and b2): C — upper bound of 5 for b1 and b2 yields epidemiologically unreasonable transmission rates, contributing to cliff-like likelihoods
- Finding 12 (Profile Construction Has Only 15 Replicates Per Rho Value): C — nprof=15 may be insufficient given ridge structure; profile may not fully maximize over nuisance parameters
- Finding 13 (Initial Conditions for E and I Hard-Coded): C — E=20 and I=10 fixed without biological justification or sensitivity check
- Finding 14 (Only One Parameter Profile Presented): C — no profile or CI for b1, b2, Phi, or eta despite these being key estimated parameters
- Finding 15 (No ARIMA/Classical Time Series Analysis): C — report goes directly from EDA to SEIR model without classical time series reference point

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "Negative Binomial Parameterization Is Epidemiologically Non-Standard — near-degenerate behavior when H≈0 creates hard numerical boundaries distorting the likelihood surface, matching the 'likelihood cliff' and stochasticity concern")
- Human Issue #3: covered (matched by finding: "Negative Binomial Parameterization Is Epidemiologically Non-Standard — code uses dnbinom with non-standard parameterization, the same measurement-model specification problem the human identifies as text/code discrepancy")
- Human Issue #4: missed
- Human Issue #5: missed

**Findings classification:**
- Finding 1 (Global search initialized from mif2 result, not base POMP object): A — major finding about initialization bug in global IF2 search; human does not raise it
- Finding 2 (Negative Binomial Parameterization Is Epidemiologically Non-Standard and Misleading): B — major finding about non-standard NegBin parameterization creating near-degenerate likelihood and non-interpretable rho (matches Human Issues #2 and #3)
- Finding 3 (No Benchmark Comparison Against Non-Mechanistic Model): A — major finding about absent baseline comparison; human does not raise it
- Finding 4 (No Model Diagnostics): A — major finding about absent diagnostic plots and ESS traces; human does not raise it
- Finding 5 (Fixed Initial Conditions Are Unjustified and Potentially Influential): A — major finding about hard-coded E(0) and I(0); human does not raise it
- Finding 6 (Profile Likelihood Seeds from Local-Search Box, Limiting Validity): A — major finding about profile being anchored to local optimum; human does not raise it
- Finding 7 (Accumulator Variable Records Recoveries, Not New Infections): C — minor finding about dN_IR vs dN_EI accumulator semantics; human does not raise it
- Finding 8 (mu_EI and mu_IR Fixed at Values That Deserve Justification): C — minor finding about unjustified fixed rate parameters; human does not raise it
- Finding 9 (Profile CI Extraction Uses Raw rho Without Enforcing Profile Maximum = Global Maximum): C — minor finding about CI cutoff referencing profile max rather than global max; human does not raise it
- Finding 10 (Computational Intensity Set to run_level = 2, Below Production Quality): C — minor finding about unconverged chains at run_level 2; human does not raise it
- Finding 11 (Global Search Box for rho Extends to 0.9 But Profile Only Covers 0.01–0.50): C — minor finding about profile grid misalignment with search box; human does not raise it
- Finding 12 (Conclusion Claims Seasonal Pattern Is Captured Without Quantitative Support): C — minor finding about unquantified seasonality claim; human does not raise it
- Finding 13 (No Assessment of R_0 or Other Epidemiologically Interpretable Quantities): C — minor finding about absent R_0 derivation; human does not raise it
- Finding 14 (Pairwise Plots for Local Search Are Based on Only 10 Points): C — minor finding about sparse pairwise scatter plot; human does not raise it
- Finding 15 (Paper Uses Single Forward Simulations for Fit Assessment): C — minor finding about nsim=1 providing weak fit evidence; human does not raise it

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by findings: "21.14.1 — profile likelihood chains fall far below the maximum, leaving sparse evaluations near the peak"; "21.14.2 — global mif2 chains spend many iterations at very low likelihoods before jumping to near -500, a 'cliff' convergence pattern"; "M1 — cooling schedule inheritance causes global chains to begin with small perturbations, explaining the cliff pattern")
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed

**Findings classification:**
- 21.14.6: A — no non-mechanistic benchmark comparison provided
- 21.14.1: B — profile likelihood for rho has most chains falling far below the maximum, leaving ~7 high-quality evaluations near the peak (matches Human Issue #2)
- 21.14.2: B — global mif2 convergence poor, especially for Phi; chains exhibit cliff-jumping pattern from -100,000 to near -500 (matches Human Issue #2)
- 21.14.7: A — no particle filter diagnostics (ESS or conditional log-likelihoods) reported
- 21.14.5: A — goodness of fit shown only via unconditioned forward simulation, not a filtering distribution conditioned on data
- 21.14.8: A — initial conditions E=20 and I=10 hardcoded without biological justification or sensitivity analysis
- 21.14.3: C — rho interpreted as reporting rate but under dnbinom's prob parameterization E[cases|H] = H*(1-rho)/rho, not rho*H
- 21.14.4: C — b1/eta trade-off visible in global pairs plot but no profile likelihoods computed for these parameters
- M1: D — cooling schedule inherited from local search reduces global exploration, explaining cliff convergence pattern (matches Human Issue #2)
- M2: C — 52-week seasonality assumption not verified by periodogram or decomposition in EDA
- Conclusion overclaiming: C — conclusion that mumps "can be well modeled" is not quantitatively substantiated without a benchmark

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 5 | 5 | 5 | 4 |
| B (AI major, human also found) | 1 | 1 | 1 | 2 |
| C (AI minor, human missed) | 6 | 9 | 9 | 4 |
| D (AI minor, human also found) | 3 | 0 | 0 | 1 |
| E (Human found, AI missed) | 1 | 4 | 3 | 4 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 1 | 3 | 1 | 4/5 = 80% | 5 | 6 | 11/15 = 73% |
| Charlie | 1 | 0 | 4 | 1/5 = 20% | 5 | 9 | 14/15 = 93% |
| Doug | 1 | 0 | 3 | 2/5 = 40% | 5 | 9 | 14/15 = 93% |
| Evan | 2 | 1 | 4 | 1/5 = 20% | 4 | 4 | 8/11 = 73% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #4: A section on potential future work can be useful, particularly given the restrictive time limitations of a course final project. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 1 out of 5 human issues (20%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #1: The project interprets the maximization difficulty in terms of the challenge of searching a large box. The local search is quite successful, with many searches jumping up to the consensus maximum around 500. The global search finds two modes, one with a reporting rate around 10% and another with a close to 100%. The latter corresponds to quite a different interpretation, where depletion of susceptibles has no dynamic importance. There is also some hint of a third mode, with even lower reporting rate. (Covered only by Alex)
- Human Issue #5: The search and results might look cleaner if phase were reparameterized to take values only in $(0,2\pi)$ since otherwise the periodicity of phase adds extra clutter to the numerical results. (Covered only by Alex)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 2 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |
