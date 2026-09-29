# Comparator Analysis — W22 Project 15

---

## Human Issues

1. The model is initialized with I=1, which may be inappropriate here. That may explain why the simulations start slower than the data. It could also seriously bias parameter estimates. Plotting the simulations and data on a log scale would help to make this evident.

2. For the delta wave, this problem is particularly acute (the omicron wave seems to start plausibly from I=1). Consequences of this can be diagnosed by the evidence of noisy likelihood maximization and high noise in the resulting simulations as they try to fit the data from an inappropriate initial condition.

3. Comparing to a benchmark likelihood, such as log-ARMA, might also have helped to identify model misspecification issues.

4. The description k = Initial infecteds does not match the code, where k is a measurement overdispersion parameter. Similarly, N is the population size not the susceptible size.

5. Fixing rho=0.1 is a strong assumption that should be relaxed later.

6. The profile likelihood should be based on a smooth curve based on the Monte Carlo point estimates. Sometimes it is helpful to plot the points, but these cannot readily give a formal interval.

7. All these issues together result in a model that gives unstable likelihood evaluation and is hard to filter and hence to obtain maximum likelihood estimates.

8. This project has apparently been carried out independently of all previous STATS/DATASCI 531 projects, but that is not entirely an advantage. There is plenty to learn from the more successful previous projects, such as https://ionides.github.io/531w21/final_project/project15/blinded.html

9. Typo in the title: "Comparsion". Many other typos may make readers wonder if the numerical work is similarly careless. Readers use easier-to-measure writing quality as a proxy for harder-to-see technical care.

10. There should be an explicit link to the data source. In reference 4, they just gave us a website about the introduction of GISAID, but it is not clear how to obtain these data.

11. The data has some questionable features. As pointed out, the author did not give a specific link to the source of the data, but if this data is true, then from the plot, we can know in March 2022, there should be neither Delta variant nor Omicron variant in the United States because their numbers both become 0, which is inconsistent with what we know. The reason for this may be that the initiative stopped classifying COVID-19 cases from a certain day, but since there is no proper source given for the data, we have no way of checking.

---

## Alex

**Coverage record:**
- Human Issue #1: covered (matched by finding: "I=1 initial condition biologically implausible, especially for mid-epidemic Omicron start")
- Human Issue #2: covered (matched by finding: "I=1 initial condition biologically implausible, especially for mid-epidemic Omicron start")
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "rho fixed at 0.1 without justification, should be estimated or justified with wave-specific statistics")
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "Np=2000 particles producing noisy likelihoods evidenced by loglik.se up to 85"; also matched by "convergence assessment qualitative only"; also matched by "only one round of mif2 per starting point")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed
- Human Issue #11: missed

**Findings classification:**
- Finding 1 (rho fixed without justification): B — rho fixed at 0.1 for both variants without wave-specific evidence (matches Human Issue #5)
- Finding 2 (Np=2000 noisy likelihoods): B — global search with only 2000 particles produces unreliable log-likelihoods (loglik.se up to 85) (matches Human Issue #7)
- Finding 3 (Delta profile does not cover MLE): A — fundamental inconsistency between global search MLE (~73) and profile CI (~100–150)
- Finding 4 (Omicron preprocessing filters weeks 1–40): A — unjustified exclusion of early Omicron data and non-comparable time axes
- Finding 5 (I=1 initial condition): B — starting from one infected in a population of 300M is implausible, especially for mid-epidemic Omicron (matches Human Issues #1 and #2)
- Finding 6 (mu_IR implausibly high for Delta): A — estimated mean infectious period ~1.3 days, biologically implausible and undiscussed
- Finding 7 (Omicron search box upper bound too narrow): A — search box capped at Beta=100 while Omicron MLE is ~389
- Finding 8 (profile plots not jointly comparable): A — faceted free-axis plots prevent verification of stated CIs; asymmetric filtering across variants
- Finding 9 (rho in partrans but never estimated): C — code applies logit transform to a fixed parameter, introducing confusion
- Finding 10 (H accumulates recoveries not incidence): C — accumulator linked to dN_IR introduces unmotivated lag not biologically justified
- Finding 11 (convergence assessment qualitative): D — no quantitative check, no cross-chain likelihood comparison (matches Human Issue #7)
- Finding 12 (guides(color=FALSE) deprecated): C — deprecated ggplot2 argument causes observed data line to render incorrectly
- Finding 13 (no vaccination/waning immunity): C — SEIR assumes fully susceptible population despite widespread vaccination during Delta wave
- Finding 14 (N=300M questionable for sequencing data): C — using total US population as susceptible pool is inconsistent with the sequenced-genome observation model
- Finding 15 (only one round of mif2): D — insufficient optimization budget for Omicron starting from poorly calibrated box (matches Human Issue #7)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Initial conditions not fully justified — I=1 and E=0 at series start are implausible and may cause early particle filter struggles")
- Human Issue #2: covered (matched by finding: "Initial conditions not fully justified — I=1 and E=0 at series start are implausible and may cause early particle filter struggles")
- Human Issue #3: covered (matched by finding: "No non-mechanistic benchmark comparison")
- Human Issue #4: missed
- Human Issue #5: covered (matched by findings: "Fixed reporting rate rho=0.1 inappropriate for sequenced GISAID data" and "rho and k both fixed without sensitivity analysis")
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "Large Monte Carlo standard errors — loglik.se = 5.58 for top Delta result — undermine likelihood comparisons")
- Human Issue #8: missed
- Human Issue #9: covered (matched by finding: "Grammar and presentation issues including 'Comparsion' title typo and numerous other errors")
- Human Issue #10: missed
- Human Issue #11: missed

**Findings classification:**
- Finding 1 (Fixed rho=0.1 inappropriate for GISAID sequenced data): B — matches Human Issue #5
- Finding 2 (Delta Beta profile CI [100,150] does not contain global MLE ~73): A
- Finding 3 (Global search second mif2 call does not re-specify Np, Nmif, rw.sd): A
- Finding 4 (No non-mechanistic benchmark comparison): B — matches Human Issue #3
- Finding 5 (Large MC standard errors — loglik.se = 5.58 — undermine likelihood comparisons): B — matches Human Issue #7
- Finding 6 (No profile likelihoods for mu_EI, mu_IR, or eta): A
- Finding 7 (rho and k both fixed without sensitivity analysis): B — matches Human Issue #5
- Finding 8 (Delta trace plot silently filters out non-converging runs below loglik > -2000): C
- Finding 9 (Initial conditions I=1 and E=0 not estimated or justified): D — matches Human Issues #1 and #2
- Finding 10 (Omicron global search box upper bound Beta=100 misaligned with best results at Beta>300): C
- Finding 11 (Delta Beta profile peak ~130 does not coincide with global MLE ~73): C
- Finding 12 (mu_IR = 5.46 implies ~1.3 day recovery time, biologically implausible for COVID-19): C
- Finding 13 (No conditional log-likelihood, ESS, or filtering distribution diagnostics): C
- Finding 14 (Omicron Beta profile resolution insufficient to precisely locate MLE): C
- Finding 15 (Grammar and presentation issues including title typo "Comparsion"): D — matches Human Issue #9

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 4 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "No Non-Mechanistic Benchmark Comparison")
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "Reporting Rate Fixed Without Justification")
- Human Issue #6: covered (matched by finding: "Delta Beta Profile Likelihood Collapses to a Singleton CI")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed
- Human Issue #11: missed

**Findings classification:**
- Major 1 (Global IF2 Search Initialized from Previous mif2 Result): A — global search inherits cooling schedule from local mif2 result, invalidating global exploration
- Major 2 (Global Search Box Excludes the MLE Region for Both Variants): A — search box too narrow; Omicron MLE at Beta=389 vs box upper bound of 100
- Major 3 (Delta Beta Profile Likelihood Collapses to a Singleton CI): B — profile is non-smooth and only one point above CI cutoff, yielding no valid interval (matches Human Issue #6)
- Major 4 (Global Search Box Excludes Delta MLE for mu_IR; Implausible mu_IR at Profile Peak): A — mu_IR MLE outside box, mu_IR=69.6 at profile peak is biologically implausible
- Major 5 (No Non-Mechanistic Benchmark Comparison): B — no ARMA or autoregressive benchmark fitted (matches Human Issue #3)
- Major 6 (Reporting Rate Fixed Without Justification): B — rho=0.1 fixed without citation or sensitivity analysis (matches Human Issue #5)
- Major 7 (Model Diagnostics Are Absent): A — no conditional log-likelihood plots, no ESS monitoring from particle filter
- Major 8 (Parameter Identifiability Not Assessed for mu_EI, mu_IR, and eta): A — profiles only computed for Beta; other parameters interpreted biologically without identifiability check
- Minor 9 (Global search size Np mismatch): C — local search uses Np=20000 but global search uses Np=2000, biasing log-likelihood comparisons
- Minor 10 ("k fixed at 10" not discussed): C — overdispersion parameter k fixed at 10 without justification or sensitivity analysis
- Minor 11 (Delta described as "most deadly variant"): C — characterization scientifically contestable and inconsistent with modeling focus on sequenced cases
- Minor 12 (Mixing of time indices across variants): C — Omicron weeks reindexed by subtracting 40 without explanation, making parameter comparisons ambiguous
- Minor 13 (filter(value>-2000) in local search plot): C — selective removal of poor chains is unreported and obscures convergence quality
- Minor 14 (Simulation plot color aesthetic bug): C — `c='black'` is not a valid ggplot2 aesthetic, leaving observed vs simulated indistinguishable
- Minor 15 (No table comparing parameter estimates): C — verbal comparisons without side-by-side MLE table with uncertainty measures
- Minor 16 (Log-likelihood comparison across variants not meaningful): C — likelihoods on different scales due to different data lengths and magnitudes

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "22.15.4 — No non-mechanistic benchmark comparison")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: covered (matched by finding: "22.15.11 — Proofreading, including 'Comparsion' in title")
- Human Issue #10: missed
- Human Issue #11: missed

**Findings classification:**
- 22.15.1: A — Likelihoods not properly evaluated via replicated pfilter; all comparisons subject to unquantified Monte Carlo error
- 22.15.2: A — Profile likelihood for Delta β is internally inconsistent; global MLE (β=73.4) falls outside the 95% CI [100,150]
- 22.15.3: A — Observation model never specified; unclear whether Poisson, Negative Binomial, or other distribution
- 22.15.4: B — No non-mechanistic benchmark comparison provided (matches Human Issue #3)
- 22.15.5: A — Biologically implausible recovery rate for Delta (μ_IR implies ~1.8-day infectious period) not flagged or discussed
- 22.15.6: C — ESS not monitored; no particle filter degeneracy diagnostic reported
- 22.15.7: C — Number of particles (Np) and global search iteration count not reported
- 22.15.8: C — Forward simulation envelopes not distinguished from filtering distribution; envelopes extremely wide
- 22.15.9: C — Reporting rate ρ=0.1 justification is incomplete; compound interpretation not acknowledged
- 22.15.10: C — β labeled "Exposure rate" (nonstandard); SEIR diagram lacks differential/difference equations
- 22.15.11: D — Proofreading: "Comparsion" in title plus multiple additional typos (matches Human Issue #9)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 9 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 5 | 3 | 5 | 4 |
| B (AI major, human also found) | 3 | 4 | 3 | 1 |
| C (AI minor, human missed) | 5 | 6 | 8 | 5 |
| D (AI minor, human also found) | 2 | 2 | 0 | 1 |
| E (Human found, AI missed) | 7 | 5 | 8 | 9 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 3 | 2 | 7 | 4/11 = 36% | 5 | 5 | 10/15 = 67% |
| Charlie | 4 | 2 | 5 | 6/11 = 55% | 3 | 6 | 9/15 = 60% |
| Doug | 3 | 0 | 8 | 3/11 = 27% | 5 | 8 | 13/16 = 81% |
| Evan | 1 | 1 | 9 | 2/11 = 18% | 4 | 5 | 9/11 = 82% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #4: The description k = Initial infecteds does not match the code, where k is a measurement overdispersion parameter. Similarly, N is the population size not the susceptible size. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #8: This project has apparently been carried out independently of all previous STATS/DATASCI 531 projects, but that is not entirely an advantage. There is plenty to learn from the more successful previous projects, such as https://ionides.github.io/531w21/final_project/project15/blinded.html (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #10: There should be an explicit link to the data source. In reference 4, they just gave us a website about the introduction of GISAID, but it is not clear how to obtain these data. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #11: The data has some questionable features. As pointed out, the author did not give a specific link to the source of the data, but if this data is true, then from the plot, we can know in March 2022, there should be neither Delta variant nor Omicron variant in the United States because their numbers both become 0, which is inconsistent with what we know. The reason for this may be that the initiative stopped classifying COVID-19 cases from a certain day, but since there is no proper source given for the data, we have no way of checking. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 4 out of 11 human issues (36%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #6: The profile likelihood should be based on a smooth curve based on the Monte Carlo point estimates. Sometimes it is helpful to plot the points, but these cannot readily give a formal interval. (Covered only by Doug)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 1 |
| Evan | 0 |
