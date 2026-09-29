# Comparator Analysis — W25 Project 03

---

## Human Issues

1. The conclusion "Our findings have important implications for public health monitoring and intervention planning" is over-stated and not supported by evidence or other lines of reasoning.

2. The phase profile is misinterpreted: "The singleton CI suggests limited identifiability — the likelihood is sharply peaked at one value. This indicates the data contains insufficient information about the seasonal timing." The sharp peak shows very strong identifiability, which might be expected from the known seasonal behavior of flu.

3. The rho profile is misinterpreted similarly. The beta0 profile is described as "smooth and fairly symmetric near the peak" when the plotted profile doesn't seem to have these properties.

4. Data of this kind can be more insightfully plotted on a log scale (presented in the project later). Also, the linear analysis (additive decomposition, periodogram, ARMA) are better on a log scale.

5. Incorrect reasoning: "the ACF plot of the log-transformed data still exhibits a slow decay, indicating that the series remains non-stationary." The usual motivation for the sample ACF assumes a stationary model.

6. The interpretation of ARMA residuals is poor, "the residuals are normally distributed but contain some extreme values." These are far from normal, and the time plot of residuals shows extreme heteroskedasticity. The residual diagnostics are trying to remind the team that they should consider a logarithmic transformation.

7. The ARMA benchmark should be carried out as log-ARMA for situations where ARMA fits better on a log scale, as in Chapter 18 (measles case study).

8. The report acknowledges previous 531 flu projects, but it does not explain its own creative contribution beyond applying similar approaches to a new dataset. There is much room for improving on previous approaches, and your own contribution should be clarified. A new dataset could involve unique modeling and inference challenges that require substantial creativity, but the report does not make that argument.

9. It is not clear what is learned from the additive decomposition that cannot be seen more clearly from other plots. To study seasonality of nonlinear and highly variable systems, a simple line plot of superposed seasonal trajectories can be more informative.

10. For comparing ARMA to SARMA it would be better to use AIC than likelihood, since degrees of freedom differ. Or make a likelihood ratio test using Wilks' approximation.

11. The conclusion "peaks occurring approximately every 60 weeks (around 1.15 years)" is curious. The data are only for about 2yr, so seasonality will not be well identified. But, if it has a relationship with the annual cycle, presumably that would be at a period of 1.0 yr.

12. Sections are numbered, but there are no figure captions or figure numbers.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding 2: "Singleton CIs Misinterpreted — phase and rho profiles both labeled 'limited identifiability' incorrectly")
- Human Issue #3: covered (matched by finding 2: "Singleton CIs Misinterpreted — rho profile misinterpreted similarly to phase")
- Human Issue #4: covered (matched by finding 8: "ARMA Differencing Applied to Wrong Series — code does not apply log transform before ARMA fitting")
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding 13: "Residual Diagnostics Are Cursory — extreme values noted but normality claim not challenged")
- Human Issue #7: covered (matched by finding 8: "ARMA Differencing Applied to Wrong Series — ARMA not done on log scale as it should be")
- Human Issue #8: covered (matched by finding 14: "SEIRS Model Borrowed Heavily from Prior Project — limited original contribution beyond cosine vs. sine swap")
- Human Issue #9: missed
- Human Issue #10: missed
- Human Issue #11: covered (matched by finding 7: "Frequency Analysis Interpretation Error — ~60-week period not reconciled with known annual flu cycle")
- Human Issue #12: missed

**Findings classification:**
- Finding 1: A — Profile likelihood methodologically flawed: single-path mif2 rather than multi-start optimization at each fixed parameter value
- Finding 2: B — Singleton CIs for phase and rho misinterpreted as "limited identifiability"; coarse grid and noisy pfilter produce the singleton, not a sharp likelihood peak (matches Human Issues #2 and #3)
- Finding 3: A — Log-likelihood comparison between ARMA (fitted to differenced data) and SEIRS POMP (fitted to original counts) is invalid across different transformations
- Finding 4: A — Data file path inconsistency: Rmd reads from ../Data/ but file lives in the project root, causing reproducibility failure
- Finding 5: A — Insufficient global search: only 10 starting points for a 13-dimensional parameter space, negligible improvement over local search
- Finding 6: A — Amplitude parameter near logit-transform constraint boundary; no discussion of whether convergence is boundary-constrained
- Finding 7: B — Frequency analysis identifies ~60-week dominant period but does not reconcile this with the known ~52-week annual flu cycle or discuss the short data span as a likely cause (matches Human Issue #11)
- Finding 8: B — ARMA differencing applied to original flu_ts not log_flu_ts despite narrative claiming log transformation; ARMA analysis effectively not done on log scale (matches Human Issues #4 and #7)
- Finding 9: C — Very small number of particles (Np=2000) used for likelihood evaluation during local search replicate comparison, introducing substantial Monte Carlo noise in trajectory selection
- Finding 10: C — Profile likelihood grid too coarse and narrow: only 10 points per profile, single noisy pfilter evaluation per point, producing unreliable CI boundaries
- Finding 11: C — Phase MLE of 52.64 weeks is nearly identical to 0.64 mod 52; the claim that global and local searches found "different seasonality patterns" is incorrect
- Finding 12: C — Initial state proportions sampled independently in global search starting design but their rw.sd is absent from the mif2 template, meaning initial conditions are fixed and not optimized
- Finding 13: D — Residual diagnostics cursory: normality claim is asserted despite extreme values; heteroskedasticity not acknowledged; Ljung-Box results not reported (matches Human Issue #6)
- Finding 14: D — SEIRS model architecture, initialization, and workflow borrowed from W24 Group 5 with only incremental modification; original analytical contribution is limited (matches Human Issue #8)
- Finding 15: C — SARMA model comparison fixes (p,q) from ARMA AIC table then searches (P,Q) separately; this sequential procedure does not guarantee the globally optimal SARMA order

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "Major Issue 3 — profile too sparse, singleton CIs for phase misinterpreted as limited identifiability"; also matched by minor finding: "singleton CIs for phase and rho attributed to identifiability")
- Human Issue #3: covered (matched by finding: "Major Issue 3 — singleton CI for rho attributed to poor identifiability without sufficient evidence"; also matched by minor finding: "singleton CIs for phase and rho attributed to identifiability")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "Major Issue 1 — log-likelihood comparison between ARMA/SARMA and POMP invalid because models fitted to different response variables")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed
- Human Issue #11: covered (matched by finding: "minor — spectral period vs. SARMA period inconsistency: 60-week dominant frequency vs. 52-week seasonal period unreconciled")
- Human Issue #12: missed

**Findings classification:**
- Major Issue 1 (invalid LL comparison — ARMA on differenced data, POMP on original): B — matches Human Issue #7
- Major Issue 2 (profile likelihood uses single pfilter per grid point, no logmeanexp): A
- Major Issue 3 (profile grid too sparse at 10 points; singleton CIs for phase and rho attributed to identifiability without supporting evidence): B — matches Human Issues #2 and #3
- Major Issue 4 (rw.sd for rho orders of magnitude below course standard, effectively freezing rho): A
- Major Issue 5 (local search best-run selection based on single noisy pfilter, not replicated logmeanexp): A
- Major Issue 6 (no convergence trace plots for global search): A
- Minor — spectral period vs. SARMA period inconsistency (60-week dominant period vs. 52-week seasonal model, unreconciled): D — matches Human Issue #11
- Minor — singleton CIs for phase and rho attributed to identifiability (likely Monte Carlo noise, not genuine likelihood property): D — matches Human Issues #2 and #3
- Minor — H accumulates I→R flow rather than E→I flow, introducing unmotivated delay: C
- Minor — global search uses only 10 starting points for 13-parameter model: C
- Minor — no biological parameter interpretation (no R0, incubation period, etc.): C
- Minor — profile likelihood covers only 4 of 8+ estimated parameters: C
- Minor — rw.sd for phase may be too small for global search given large initialization range: C
- Minor — missing model diagnostics (no ESS traces, no conditional log-likelihoods): C
- Minor — data path error (`../Data/flu_michigan.csv`) prevents reproduction: C

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding 8: "ARMA/SARMA fitted to differenced data rather than log-transformed data — log transformation abandoned")
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding 8: same finding — ARMA fitted to differenced not log-transformed data, benchmark should use log scale")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed
- Human Issue #11: covered (matched by finding 9: "periodogram identifies ~60-week period from fewer than 2 full cycles, inconsistent with annual flu seasonality")
- Human Issue #12: missed

**Findings classification:**
- Finding 1 (accumulator tracks recoveries not infections): A — semantic mismatch in rprocess accumulator; no human issue raised this
- Finding 2 (invalid log-likelihood comparison ARMA/SARMA vs POMP): A — likelihoods on different data and distributional families; human issue #10 asks about AIC vs likelihood for ARMA-to-SARMA comparison, a distinct specific claim
- Finding 3 (profile likelihood is single-path, not true profile): A — single IF2 run from single start, single pfilter evaluation; no human issue raised this
- Finding 4 (global search 10 replicates with Nmif=50 insufficient): A — convergence not confirmed; no human issue raised this
- Finding 5 (rho profile range ±20% far too narrow): A — singleton CI artifact of grid range; no human issue raised this (human issues #2/#3 address misinterpretation of identifiability, not the grid range methodology)
- Finding 6 (no benchmark comparison on same data): A — no valid quantitative comparison against non-mechanistic model; no human issue raised this
- Finding 7 (no quantitative model diagnostics beyond visual inspection): A — no conditional log-likelihoods, ESS, or simulation summary statistics; no human issue raised this
- Finding 8 (ARMA/SARMA fitted to differenced not log-transformed data): D — matches Human Issues #4 and #7
- Finding 9 (periodogram frequency interpretation questionable): D — matches Human Issue #11
- Finding 10 (amp logit constraint noted): C — minor note that constraint is correctly implemented; no human issue raised this
- Finding 11 (phase grid may wrap around 52-week periodicity): C — profile grid spans the periodicity boundary; no human issue raised this
- Finding 12 (only 4 of 13 parameters profiled): C — key parameters like mu_EI and mu_RS omitted; no human issue raised this
- Finding 13 (parameter estimates not compared to biological knowledge): C — rho remarkably small and not discussed; no human issue raised this
- Finding 14 (data path hard-coded as ../Data/): C — reproducibility concern; no human issue raised this
- Finding 15 (single pfilter per profile grid point introduces Monte Carlo noise): C — profile curves unreliable due to noise; no human issue raised this

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 9 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "25.03.2 — profile likelihood under-powered; singleton CIs for phase and rho wrongly interpreted as evidence of unidentifiability")
- Human Issue #3: covered (matched by finding: "25.03.2 — profile likelihood under-powered; singleton CIs for phase and rho wrongly interpreted as evidence of unidentifiability")
- Human Issue #4: covered (matched by finding: "25.03.4 — log transformation described but ARMA fitting applied to raw non-log-transformed differenced counts")
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "25.03.4 — log transformation described but ARMA fitting applied to raw non-log-transformed differenced counts")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed
- Human Issue #11: missed
- Human Issue #12: missed

**Findings classification:**
- 25.03.1: A — log-likelihood comparison between ARIMA (fit to differenced raw counts) and POMP (fit to raw counts) is across incompatible scales and uninterpretable
- 25.03.2: B — profile likelihood under-powered (10 grid points, single mif2 path per point); singleton CIs for phase and rho wrongly interpreted as unidentifiability (matches Human Issues #2 and #3)
- 25.03.5: A — no particle filter diagnostics (ESS plots, per-step conditional log-likelihoods) are present
- 25.03.14: A — no profile likelihood computed for transition rate parameters mu_EI, mu_IR, mu_RS
- 25.03.3: C — initial condition parameters S0, E0, I0, R0 have no rw.sd entries and are effectively fixed during mif2, but presented as estimated
- 25.03.4: D — log transformation described in Section 3 but all ARMA/SARMA fitting applied to raw non-log-transformed differenced counts (matches Human Issues #4 and #7)
- 25.03.7: C — single pfilter evaluation used to select the best local mif2 run, introducing Monte Carlo noise into the selection step
- 25.03.6: C — reporting rate rho ≈ 0.00015 (1 in 6,000 infections captured) not compared to published influenza ascertainment estimates
- 25.03.15: C — pair plots based on only 10 runs are too noisy to support identifiability conclusions

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 5 | 4 | 7 | 3 |
| B (AI major, human also found) | 3 | 2 | 0 | 1 |
| C (AI minor, human missed) | 5 | 7 | 6 | 4 |
| D (AI minor, human also found) | 2 | 2 | 2 | 1 |
| E (Human found, AI missed) | 5 | 8 | 9 | 8 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 3 | 2 | 5 | 7/12 = 58% | 5 | 5 | 10/15 = 67% |
| Charlie | 2 | 2 | 8 | 4/12 = 33% | 4 | 7 | 11/15 = 73% |
| Doug | 0 | 2 | 9 | 3/12 = 25% | 7 | 6 | 13/15 = 87% |
| Evan | 1 | 1 | 8 | 4/12 = 33% | 3 | 4 | 7/9 = 78% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #1: The conclusion "Our findings have important implications for public health monitoring and intervention planning" is over-stated and not supported by evidence or other lines of reasoning. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #5: Incorrect reasoning: "the ACF plot of the log-transformed data still exhibits a slow decay, indicating that the series remains non-stationary." The usual motivation for the sample ACF assumes a stationary model. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #9: It is not clear what is learned from the additive decomposition that cannot be seen more clearly from other plots. To study seasonality of nonlinear and highly variable systems, a simple line plot of superposed seasonal trajectories can be more informative. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #10: For comparing ARMA to SARMA it would be better to use AIC than likelihood, since degrees of freedom differ. Or make a likelihood ratio test using Wilks' approximation. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #12: Sections are numbered, but there are no figure captions or figure numbers. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 5 out of 12 human issues (42%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #6: The interpretation of ARMA residuals is poor, "the residuals are normally distributed but contain some extreme values." These are far from normal, and the time plot of residuals shows extreme heteroskedasticity. The residual diagnostics are trying to remind the team that they should consider a logarithmic transformation. (Covered only by Alex)
- Human Issue #8: The report acknowledges previous 531 flu projects, but it does not explain its own creative contribution beyond applying similar approaches to a new dataset. There is much room for improving on previous approaches, and your own contribution should be clarified. A new dataset could involve unique modeling and inference challenges that require substantial creativity, but the report does not make that argument. (Covered only by Alex)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 2 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |
