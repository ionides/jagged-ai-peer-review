# Comparator Analysis — W21 Project 16

---

## Human Issues

1. The project acknowledges that the computation put into maximizing the stochastic volatility model might be insufficient - for example, there is a trend in the likelihood against H_0 suggesting that more searching would yield gains. However, an advantage of GARCH is that it is quicker to compute with.

2. This analysis does not add much insight on previous cited projects. Is there some way to frame a question that goes beyond comparing GARCH vs stochastic volatility with leverage?

3. The POMP modeling part of project looks to be carried out hastily. The profile shows evidence for phi < 1, but that does not make the likelihood for phi=1 "unstable", just lower. The profile is a better search than the local investigation, and even finds a slightly higher likelihood than the global search - the maximized profile likelihood should be taken as the new estimate of the MLE.

---

## Alex

**Coverage record:**
- Human Issue #1: covered (matched by findings: "Computational settings too low and acknowledged but not improved" and "Profile uses nprof=2 profiles per phi value, too sparse")
- Human Issue #2: missed
- Human Issue #3: covered (matched by findings: "Profile likelihood section contains incomplete statement and rendering error — 'unstable' claim is wrong"; "Global search box for phi constrained to [0.9950, 0.9999], precluding discovery of other optima, while profile finds higher likelihoods"; "Profile inconsistency with global search constraints — profile explores wider phi range than box search")

**Findings classification:**
- Finding 1 (profile rendering error / "unstable" claim): B — profile likelihood section has missing phi value and erroneous "unstable" claim (matches Human Issue #3)
- Finding 2 (POMP fitted to simulated data only): A — particle filter evaluated on simulated dataset, not observed returns; not raised by human
- Finding 3 (POMP vs GARCH log-likelihood not comparable): A — likelihoods on different footing but comparison made anyway; not raised by human
- Finding 4 (global search phi constrained to [0.9950, 0.9999]): B — tight constraint prevents finding true MLE; profile finds higher likelihood than global search (matches Human Issue #3)
- Finding 5 (profile inconsistency with global search constraints): B — profile explores much wider phi range than global search box; paper does not reconcile (matches Human Issue #3)
- Finding 6 (demeaning not justified): A — pre-demeaning interacts with POMP mean structure but is unmotivated; not raised by human
- Finding 7 (computational settings too low, acknowledged but not improved): B — Np=2000, Nmif=50 insufficient for reliable convergence (matches Human Issue #1)
- Finding 8 (ACF used to claim independence incorrectly): C — absence of linear ACF does not imply independence; not raised by human
- Finding 9 (GARCH equation omits alpha0): C — written fitted model drops intercept; not raised by human
- Finding 10 (demeaned return plot no x-axis date labels): C — plotted against integer index instead of calendar time; not raised by human
- Finding 11 (log-price plot double log transformation): C — log("y") applied to already log-transformed values; not raised by human
- Finding 12 (profile uses nprof=2, too sparse): D — only 2 restarts per phi grid point; insufficient computational effort for reliable profile envelope (matches Human Issue #1)
- Finding 13 (no simulation study or posterior predictive check): C — simulator built but never used for model checking; not raised by human
- Finding 14 (conclusion claims positive volatility shift, unsupported): C — GARCH parameters imply mean-reversion, not positive drift; not raised by human
- Finding 15 (references misattribute student projects to Ionides): C — citation error; not raised by human

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 4 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 1 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: covered (matched by finding: "global search phi box too narrow relative to profile range")
- Human Issue #2: missed
- Human Issue #3: covered (matched by findings: "profile conclusion incomplete — phi MLE missing, 'unstable' characterization wrong" and "global search phi box too narrow relative to profile range")

**Findings classification:**
- Major Issue 1 (ACF independence conclusion; missing ARCH-effect diagnostic): A — incorrect independence conclusion from ACF; ACF of squared returns missing
- Major Issue 2 (POMP underperforms GARCH; wrong response recommended): A — authors recommend more computation rather than model revision
- Major Issue 3 (Profile likelihood incomplete; phi MLE missing from text): B — phi MLE absent from text, "unstable" characterization wrong, no CI stated (matches Human Issue #3)
- Major Issue 4 (No simulation-based model diagnostics): A — no forward simulation, no ESS monitoring, no conditional log-likelihoods
- Major Issue 5 (Global search phi box too narrow vs. profile range): B — box (0.9950, 0.9999) inconsistent with profile range (0.80, 0.9999); profile finds higher likelihood than global search (matches Human Issues #1 and #3)
- Major Issue 6 (Convergence diagnostics not discussed): A — trace plots generated but never interpreted in text
- Minor: Missing GARCH intercept: C — omega term omitted from GARCH(1,1) equation
- Minor: Double-logarithm in exploratory plot: C — log(Price) plotted with log="y" axis, applying log twice
- Minor: Heavy-tailed residuals inadequately addressed: C — QQ-plot tails noted but explanation vague; Student-t innovations not considered
- Minor: Local search uses single starting parameter set: C — all 20 mif2 runs start from same params_test
- Minor: AIC not used for POMP vs. GARCH comparison: C — parameter count difference not accounted for in log-likelihood comparison
- Minor: tseries::garch vs. fGarch::garchFit: C — different packages used for model selection and fitting without verifying normalization consistency
- Minor: Data description ambiguity: C — "weekly average closing price" vs. end-of-week closing price
- Minor: Profile nprof=2 sparse: C — only 2 optimization starts per phi grid point may miss true maximum

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 1 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: covered (matched by findings: "Global search initialized from prior IF2 result", "Profile likelihood: only nprof=2 starts per grid point", "Profile likelihood: phi not fixed in rw.sd / profile anti-pattern", "POMP fails to beat GARCH without acknowledging computational limitations", "Inadequate number of particles and iterations")
- Human Issue #2: missed
- Human Issue #3: missed

**Findings classification:**
- Finding 1 (Global search initialized from prior IF2 result): B — global search inherits cooling state of local chain, invalidating global coverage claim (matches Human Issue #1)
- Finding 2 (Profile likelihood: phi not fixed in rw.sd / profile also uses if1[[1]] anti-pattern): B — profile optimization also improperly initialized and suffers same computational deficiency as global search (matches Human Issue #1)
- Finding 3 (Profile likelihood: only nprof=2 starts per grid point): B — too few starts for reliable constrained optimization, making profile and any derived CI unreliable (matches Human Issue #1)
- Finding 4 (Incomplete sentence in conclusion — placeholder result): A — "phi = " with no value filled in; this placeholder finding is not raised by any human issue
- Finding 5 (POMP fails to beat GARCH without acknowledging computational limitations): B — AIC comparison ignores Monte Carlo noise and the unreliable global search initialization; computational shortcomings undermine the conclusion (matches Human Issue #1)
- Finding 6 (Inadequate number of particles and iterations): B — Np=2000, Nmif=50, profile Np=1000 insufficient for reliable inference; convergence not discussed (matches Human Issue #1)
- Finding 7 (No model diagnostics beyond visual convergence traces): A — no ESS plots, conditional log-likelihood, or simulated trajectory comparisons; not raised by any human issue
- Finding 8 (Profile likelihood plot: maximum phi value missing, confidence interval not reported): A — profile contributes no interpretable scientific content without bounds; not raised by any human issue
- Finding 9 (Stationarity claim without formal test): C — visual ACF inspection used to assert independence without ADF/KPSS; not raised by any human issue
- Finding 10 (GARCH AIC table starts at p=1, q=1; no p=0 or q=0 rows): C — simpler submodels excluded from AIC comparison; not raised by any human issue
- Finding 11 (QQ-plot explanation is superficial): C — heavy tails attributed to sample bias rather than inherent leptokurtosis; not raised by any human issue
- Finding 12 (Missing AIC comparison for POMP): C — comparison done by log-likelihood only without adjusting for parameter count difference; not raised by any human issue
- Finding 13 (Data description inconsistency — 570 vs 569): C — text states 570 observations but model is fitted to 569 returns; not raised by any human issue
- Finding 14 (rw.sd values identical for all regular parameters): C — uniform rw.sd=0.02 applied across parameters on very different scales; not raised by any human issue
- Finding 15 (No benchmark comparison against ARMA baseline): C — no ARMA on squared/absolute returns as simpler non-mechanistic comparison; not raised by any human issue

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 5 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: covered (matched by finding: "convergence diagnostics absent — gap between local and global search suggests non-convergence, consistent with insufficient optimization")
- Human Issue #2: missed
- Human Issue #3: missed

**Findings classification:**
- 21.16.1: A — log-likelihood comparison between GARCH and POMP is not validated (different conventions, MC variance)
- 21.16.3: B — convergence diagnostics absent from rendered output; gap between local (1244) and global (1264) search suggests non-convergence (matches Human Issue #1)
- 21.16.2: A — profile likelihood for phi likely does not correctly fix phi; nprof=2 too sparse
- 21.16.4: C — pfilter in Section 4.1 evaluates simulated data, not real SSE data
- 21.16.6: C — ACF conclusion overstated; only checks linear dependence, not volatility clustering
- 21.16.7: C — missing phi value in text (knitting artifact)
- 21.16.13: C — GARCH equation omits alpha_0 (omega intercept)
- 21.16.5: C — no ESS monitoring during filtering
- Underdeveloped (sigma_nu): C — global search box excludes sigma_nu=0, so leverage-free model is never explored

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 2 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 3 | 4 | 3 | 2 |
| B (AI major, human also found) | 4 | 2 | 5 | 1 |
| C (AI minor, human missed) | 7 | 8 | 7 | 6 |
| D (AI minor, human also found) | 1 | 0 | 0 | 0 |
| E (Human found, AI missed) | 1 | 1 | 2 | 2 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 4 | 1 | 1 | 2/3 = 67% | 3 | 7 | 10/15 = 67% |
| Charlie | 2 | 0 | 1 | 2/3 = 67% | 4 | 8 | 12/14 = 86% |
| Doug | 5 | 0 | 2 | 1/3 = 33% | 3 | 7 | 10/15 = 67% |
| Evan | 1 | 0 | 2 | 1/3 = 33% | 2 | 6 | 8/9 = 89% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #2: This analysis does not add much insight on previous cited projects. Is there some way to frame a question that goes beyond comparing GARCH vs stochastic volatility with leverage? (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 1 out of 3 human issues (33%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

(none)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |
