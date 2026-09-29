# Comparator Analysis — W22 Project 12

---

## Human Issues

1. For the mechanistic model, one either has to analyze cases summed over weeks or to explicitly model the weekly periodicity.

2. Compare the mechanistic fit likelihoods to the ARMA benchmark.

3. For the ADF test, it is best not to present unprocessed R output. Better still, one could avoid the test entirely. ADF is only a test against a unit root hypothesis. Simply plotting the data would be better to detect a wider range of phenomena that might suggest a nonstationary model.

4. In the ARIMA model for the full data, the formula of the ARIMA is wrong. It should be $\phi(B)(\nabla^d Y_n - \mu)= \psi(B)\epsilon_n$.

5. Fig 14 shows clearly how the initial values are inappropriately specified for the model. Also, how the model fails to capture the week day effect in the data. The model has to compensate for these shortcomings by having a large amount of noise in order to do its best to fit the data.

6. The fixed choices $E_0=30000$ and $I_0=15000$ are not discussed - one must go to the code to find them. However, these unsuccessful choices critically affect all the other model-based analysis. Better to estimate them from data.

7. The model has measurement overdispersion, but no process noise (see Chapter 17).

---

## Alex

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Weekly seasonality is identified but never modeled")
- Human Issue #2: covered (matched by finding: "No comparison of SEIR likelihood to a null or baseline")
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "Weekly seasonality is identified but never modeled"; also matched by finding: "E and I initial conditions are fixed at arbitrary values")
- Human Issue #6: covered (matched by finding: "E and I initial conditions are fixed at arbitrary values")
- Human Issue #7: missed

**Findings classification:**
- Finding 1 (beta switch threshold): A — hard-coded, unjustified t>33 threshold for transmission rate switch
- Finding 2 (mu_EI/mu_IR fixed): A — mu_EI and mu_IR fixed without justification or profile likelihood
- Finding 3 (dmeas/rmeas inconsistency): A — measurement model variance formula differs between dmeas and rmeas
- Finding 4 (global search box): A — global search box excludes parameter values explored in local search; rho hits upper boundary
- Finding 5 (particle filter SE): A — particle filter SE very large (4.77) at initial guess; Np not increased for search
- Finding 6 (no profile likelihood/CIs): A — no profile likelihoods or confidence intervals for any SEIR parameter
- Finding 7 (local search Nmif=50): C — 20 chains with Nmif=50 insufficient for 5-dimensional optimization
- Finding 8 (ARIMA conflates selection/validation): C — ARIMA analysis conflates model selection with model validation
- Finding 9 (weekly seasonality unmodeled): D — weekly seasonality identified but never modeled (matches Human Issues #1 and #5)
- Finding 10 (E/I initial conditions): D — E and I initial conditions fixed at arbitrary values without justification (matches Human Issues #5 and #6)
- Finding 11 (incomplete sentence): C — incomplete sentence fragment in text indicates lack of proofreading
- Finding 12 (Figure 10 caption): C — Figure 10 caption incorrectly describes the plot
- Finding 13 (global search filter): C — global search pairs plot filter threshold of 100000 is trivially permissive
- Finding 14 (dual data sources): C — data read from two sources inconsistently without explanation
- Finding 15 (no SEIR vs baseline comparison): D — no comparison of SEIR likelihood to ARIMA or null baseline (matches Human Issue #2)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 3 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "No benchmark comparison to non-mechanistic model")
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "Initial compartment values E=30000 and I=15000 fixed without justification")
- Human Issue #6: covered (matched by finding: "Initial compartment values E=30000 and I=15000 fixed without justification")
- Human Issue #7: missed

**Findings classification:**
- Finding 1 (dmeasure/rmeasure inconsistent variance formulas): A — measurement model code inconsistency between dmeasure and rmeasure
- Finding 2 (H accumulates dN_IR instead of infections): A — structural misspecification linking recoveries to observations
- Finding 3 (no profile likelihood): A — profile likelihoods absent for all parameters
- Finding 4 (global search Nmif=50 insufficient): A — computational effort inadequate for reliable MLE
- Finding 5 (mu_EI and mu_IR fixed without sensitivity analysis): A — transition rate parameters fixed without sensitivity check
- Finding 6 (no benchmark comparison to ARMA): B — no quantitative likelihood comparison between SEIR and ARIMA (matches Human Issue #2)
- Finding 7 (beta switch at t=33 hardcoded): A — deterministic structural break unestimated and unjustified
- Finding 8 (normal approximation for count data): C — Gaussian measurement model inappropriate for count data
- Finding 9 (Figure 10 labeled incorrectly): C — caption says Omicron subset but code fits full dataset
- Finding 10 (scatterplot filter loglik-100000 is vacuous): C — filter threshold retains essentially all points
- Finding 11 (E=30000 and I=15000 fixed without justification): D — initial compartment values fixed, unmotivated, not estimated (matches Human Issues #5 and #6)
- Finding 12 (ACF plots mislabeled as autocovariance): C — terminology error in figure labels
- Finding 13 (incomplete sentence in Omicron seasonality section): C — drafting artifact, incomplete sentence
- Finding 14 (ARIMA defaults to ARIMA(5,1,5) without seasonal modeling): C — ARIMA model selection ignores weekly seasonal structure
- Finding 15 (conclusion overstates SEIR success): C — qualitative claim of SEIR superiority is unsubstantiated

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "No benchmark comparison between the SEIR model and a non-mechanistic baseline")
- Human Issue #3: covered (matched by finding: "Stationarity test conclusion is incorrectly framed")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed

**Findings classification:**
- Finding 1 (Global search initialized from previous mif2 result): A — global search anti-pattern, cooling schedule inherited from local chain
- Finding 2 (MLE for beta1 lies outside global search box): A — binding box constraint produces constrained optimum
- Finding 3 (rho concentrates at boundary near 1): A — rho pinned at upper bound, scientifically implausible
- Finding 4 (dmeasure and rmeasure use inconsistent variance formulas): A — psi*H vs psi*rho*H mismatch in overdispersion term
- Finding 5 (No benchmark comparison between SEIR model and non-mechanistic baseline): B — ARIMA log-likelihoods not used as quantitative benchmark for SEIR (matches Human Issue #2)
- Finding 6 (No profile likelihoods; parameter identifiability unassessed): A — no profiles for rho or psi
- Finding 7 (Accumulator H tracks recoveries not new detected cases): A — H accumulates dN_IR rather than new infection/detection flow
- Finding 8 (Hard-coded breakpoint for beta transition without justification): C — t=33 threshold not estimated or sensitivity-tested
- Finding 9 (Stationarity test conclusion is incorrectly framed): D — ADF rejection on differenced series misread; same misuse-of-ADF concern as human (matches Human Issue #3)
- Finding 10 (AIC table caption mislabels Figure 10): C — figure number not filled in, proofreading error
- Finding 11 (Particle filter SE large at initial parameter values): C — SE of 4.77 indicates poor fit region at starting values
- Finding 12 (ARIMA same model order for full dataset and Omicron subset without discussion): C — coincident ARIMA(5,1,5) on very different data windows, possible overfitting
- Finding 13 (No model diagnostics beyond pairs scatter plot): C — no conditional log-likelihood plots or ESS at MLE
- Finding 14 (mu_EI and mu_IR fixed without sensitivity analysis): C — transition rates fixed, no sensitivity exploration of R0 implications
- Finding 15 (No forecast or prediction from fitted model): C — no probabilistic forecasts generated from filtering distribution

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "22.12.1 — Missing benchmark comparison: SEIR log-likelihood never compared to ARIMA")
- Human Issue #3: covered (matched by finding: "22.12.6 — ADF test applied to already-differenced series, circular reasoning")
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "Initial compartment values E=30000, I=15000 not justified")
- Human Issue #6: covered (matched by finding: "Initial compartment values E=30000, I=15000 not justified")
- Human Issue #7: missed

**Findings classification:**
- 22.12.1: B — no quantitative ARIMA vs SEIR log-likelihood comparison made (matches Human Issue #2)
- 22.12.2: A — dmeas and rmeas implement different variance formulas, inconsistency between filter density and forward simulator
- 22.12.3: A — no profile likelihoods or confidence intervals; rho piles up at boundary without investigation
- 22.12.7: A — fixed mu_EI and mu_IR throughout with no sensitivity analysis
- 22.12.5: C — potential under-convergence in global search; IF2 chains not settled by iteration 50
- 22.12.6: D — ADF test applied to already-differenced series, making the argument circular (matches Human Issue #3)
- ESS collapse: C — ESS near zero at t=120–134 suggests model difficulty tracking descent phase
- Hard-coded regime change at t=33: C — beta regime switch hard-coded without sensitivity analysis or data justification
- Initial compartment values E=30000, I=15000 not justified: D — hard-coded without reference to data or prior estimates (matches Human Issues #5 and #6)
- rho at boundary signals misspecification: C — rho MLE ≈ 0.995 epidemiologically implausible, suggests model absorbing unexplained variation

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 6 | 6 | 6 | 3 |
| B (AI major, human also found) | 0 | 1 | 1 | 1 |
| C (AI minor, human missed) | 6 | 7 | 7 | 4 |
| D (AI minor, human also found) | 3 | 1 | 1 | 2 |
| E (Human found, AI missed) | 3 | 4 | 5 | 3 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 0 | 3 | 3 | 4/7 = 57% | 6 | 6 | 12/15 = 80% |
| Charlie | 1 | 1 | 4 | 3/7 = 43% | 6 | 7 | 13/15 = 87% |
| Doug | 1 | 1 | 5 | 2/7 = 29% | 6 | 7 | 13/15 = 87% |
| Evan | 1 | 2 | 3 | 4/7 = 57% | 3 | 4 | 7/10 = 70% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #4: In the ARIMA model for the full data, the formula of the ARIMA is wrong. It should be $\phi(B)(\nabla^d Y_n - \mu)= \psi(B)\epsilon_n$. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #7: The model has measurement overdispersion, but no process noise (see Chapter 17). (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 2 out of 7 human issues (29%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #1: For the mechanistic model, one either has to analyze cases summed over weeks or to explicitly model the weekly periodicity. (Covered only by Alex)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 1 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |
