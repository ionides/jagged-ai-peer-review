# Ned-Clean Analysis — W21 Project 16

---

## Human Issues

1. Computation for the stochastic volatility model may be insufficient — the likelihood trend against H_0 suggests more searching would yield gains.
2. The analysis does not add much insight beyond previous cited projects; the framing does not go beyond comparing GARCH vs stochastic volatility with leverage.
3. The POMP modeling appears hastily carried out: the profile shows evidence for phi < 1 but this does not make the likelihood for phi=1 "unstable," just lower; the profile is a better search than the local investigation and even finds a slightly higher likelihood than the global search, so the maximized profile likelihood should be taken as the new estimate of the MLE.

---

## Alex

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Computational settings are too low and this is acknowledged but not improved")
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "Profile likelihood section contains an incomplete statement and a rendering error — 'likelihood becomes unstable' claim directly contradicted")

**Findings classification:**
- Alex #1 (Profile rendering error and 'unstable' claim): B — matches Human Issue #3
- Alex #2 (POMP particle filter never fits real data): A — POMP pfilter on simulated data, not Shanghai returns
- Alex #3 (POMP log-likelihood not comparable to GARCH): A — likelihoods on different footings (exact vs MC estimate)
- Alex #4 (Global search box for phi too narrow [0.9950, 0.9999]): A — precludes finding true MLE; profile shows higher likelihoods outside this range
- Alex #5 (Profile likelihood does not fix phi): A — phi not in rw.sd but profile initialization has duplicate-name ambiguity
- Alex #6 (Demeaning returns not justified): A — questionable data transformation not discussed
- Alex #7 (Computational settings too low): B — matches Human Issue #1
- Alex #8 (ACF incorrectly claims independence): C — absence of linear autocorrelation does not imply independence
- Alex #9 (GARCH equation omits alpha_0): C — intercept missing from written model formula
- Alex #10 (Demeaned return plot lacks date labels): C — plotted against integer index, not calendar time
- Alex #11 (Double log transformation coding error): C — log("y") applied to already-log-transformed values
- Alex #12 (Profile uses nprof=2, too sparse): C — only 2 restarts per phi grid point
- Alex #13 (No simulation-based model validation): C — simulator used only for pfilter check, not for goodness-of-fit
- Alex #14 (Conclusion claims positive volatility drift): C — claim not supported by GARCH(1,1) analysis
- Alex #15 (References misattribute student projects to Ionides): C — citation error affecting four references

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 1 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: covered (matched by finding: "POMP Fails to Beat GARCH Benchmark; response inadequate — authors attribute gap solely to computation without model diagnostics")
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "Profile Likelihood: Profiled Parameter (phi) Not Fixed in rw.sd, allowing it to drift — profile technically invalid")

**Findings classification:**
- Charlie #1 (Global search initialized from prior mif2 result): A — anti-pattern; cooling schedule inherited, global coverage not achieved
- Charlie #2 (Profile phi not fixed in rw.sd): B — matches Human Issue #3
- Charlie #3 (Profile nprof=2 too sparse): A — only 100 total profile runs across 50 grid points
- Charlie #4 (Incomplete sentence / missing phi value): A — placeholder result never filled in before submission
- Charlie #5 (POMP fails GARCH, response inadequate): B — matches Human Issue #1
- Charlie #6 (pfilter in profile evaluates mif2 result, not base pomp object): A — likelihood evaluated at potentially drifted parameters
- Charlie #7 (No model diagnostics beyond convergence traces): A — no ESS, no conditional log-likelihood plots, no simulation comparison
- Charlie #8 (pfilter run on sim1.filt, not Shanghai.filt): C — particle filter section uses simulated data
- Charlie #9 (ACF independence claim overstated): C — ACF of squared returns not checked
- Charlie #10 (GARCH AIC uses tseries non-standard normalization): C — AIC table and POMP comparison may not be on same scale
- Charlie #11 (phi box constraint extremely narrow): C — global search box forces phi near 1
- Charlie #12 (No simulation-based model validation): C — no overlay of simulated vs observed trajectories
- Charlie #13 (Profile phi range may not include MLE): C — global box [0.9950, 0.9999] inconsistent with profile range [0.80, 0.99999]
- Charlie #14 (Missing parameter estimates table): C — no table of MLE values for all six parameters
- Charlie #15 (Causal language and mischaracterized GARCH conclusion): C — "volatility should slightly shift positively" unsupported by stationary GARCH(1,1)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 1 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Inadequate Number of Particles and Iterations for Reliable Inference")
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "Profile Likelihood: Profiled Parameter (phi) Not Fixed in rw.sd")

**Findings classification:**
- Doug #1 (Global search initialized from prior IF2 result): A — replicates inherit cooling schedule of local chain; global coverage not achieved
- Doug #2 (Profile phi not fixed in rw.sd): B — matches Human Issue #3
- Doug #3 (Profile nprof=2 too sparse): A — only 100 total runs for 50 grid points
- Doug #4 (Incomplete sentence / placeholder result): A — phi value at profile maximum missing from text
- Doug #5 (POMP fails to beat GARCH without acknowledging computational limits): A — comparison ignores MC noise, global search initialization flaw
- Doug #6 (Inadequate particles and iterations): B — matches Human Issue #1
- Doug #7 (No model diagnostics): A — no ESS, no conditional log-likelihood, no simulation comparison
- Doug #8 (Profile max phi missing, CI not reported): A — profile analysis contributes no interpretable scientific content
- Doug #9 (Stationarity claim without formal test): C — visual ACF inspection only; no ADF/KPSS
- Doug #10 (GARCH AIC table missing p=0/q=0 rows): C — simpler submodels excluded from comparison
- Doug #11 (QQ-plot explanation superficial): C — attributes heavy tails to sample bias rather than leptokurtosis
- Doug #12 (Missing AIC for POMP): C — no AIC comparison adjusting for parameter count difference (3 vs 6)
- Doug #13 (Data description inconsistency): C — 570 observations stated but 569 returns used in model
- Doug #14 (rw.sd values identical for all parameters): C — uniform 0.02 perturbation across parameters on very different scales
- Doug #15 (No ARMA baseline): C — no simpler non-mechanistic benchmark for squared/absolute returns

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 1 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Convergence diagnostics absent from rendered output — gap between local (1244) and global (1264) suggests non-convergence")
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "Profile likelihood for phi likely does not correctly fix phi — initialization inconsistency and nprof=2 too sparse")

**Findings classification:**
- Evan #1 / ID 21.16.1 (Log-likelihood comparison not validated): A — GARCH exact vs POMP MC estimate; 5.5-unit difference within MC noise range
- Evan #2 / ID 21.16.3 (Convergence diagnostics absent): B — matches Human Issue #1
- Evan #3 / ID 21.16.2 (Profile phi likely not correctly fixed): B — matches Human Issue #3
- Evan #4 / ID 21.16.4 (pfilter evaluates simulated data, Minor escalated): C — Section 4.1 pfilter on sim1.filt, not real SSE data
- Evan #5 / ID 21.16.6 (ACF conclusion overstated): C — independence claim overreaches; squared returns not checked
- Evan #6 / ID 21.16.7 (Missing phi value in text): C — knitting artifact; phi blank in conclusion sentence
- Evan #7 / ID 21.16.13 (GARCH equation omits alpha_0): C — omega/intercept term missing from reported equation
- Evan #8 / ID 21.16.5 (No ESS monitoring): C — particle diversity not checked for leverage model
- Evan #9 (sigma_nu box constraint underdeveloped): C — sigma_nu=0 (no leverage) never explored; profile over sigma_nu absent

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 1 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 1 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 5 | 5 | 6 | 1 |
| B (AI major, human also found) | 2 | 2 | 2 | 2 |
| C (AI minor, human missed) | 8 | 8 | 7 | 6 |
| D (AI minor, human also found) | 0 | 0 | 0 | 0 |
| E (Human found, AI missed) | 1 | 1 | 1 | 1 |

---

## Per-Reviewer Metrics

Human Issues total: 3

**Alex**
- Human Recall = (B+D) / (B+D+E) = (2+0) / (2+0+1) = 2/3 = 67%
- AI-Unique Rate = (A+C) / (A+B+C+D) = (5+8) / (5+2+8+0) = 13/15 = 87%

**Charlie**
- Human Recall = (B+D) / (B+D+E) = (2+0) / (2+0+1) = 2/3 = 67%
- AI-Unique Rate = (A+C) / (A+B+C+D) = (5+8) / (5+2+8+0) = 13/15 = 87%

**Doug**
- Human Recall = (B+D) / (B+D+E) = (2+0) / (2+0+1) = 2/3 = 67%
- AI-Unique Rate = (A+C) / (A+B+C+D) = (6+7) / (6+2+7+0) = 13/15 = 87%

**Evan**
- Human Recall = (B+D) / (B+D+E) = (2+0) / (2+0+1) = 2/3 = 67%
- AI-Unique Rate = (A+C) / (A+B+C+D) = (1+6) / (1+2+6+0) = 7/9 = 78%

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #2: The analysis does not add much insight beyond previous cited projects; the framing does not go beyond comparing GARCH vs stochastic volatility with leverage.

**Count: 1 out of 3 (33%)**

### Unique finds per reviewer

Human issues covered by only one reviewer and missed by all others: none. Both covered issues (#1 and #3) were addressed by all four reviewers.

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |

### Universal AI-only flags

Issues raised by every reviewer that the human did not mention:

All four reviewers raised the following concerns not found in the human review:

1. Global search initialized from prior mif2/IF2 result object rather than the base pomp object (anti-pattern causing ineffective global search). Raised by Charlie, Doug, and Evan (Alex framed this differently as the global box being too narrow, but did not raise the initialization anti-pattern explicitly). Strictly universal across Charlie, Doug, Evan (3 of 4 reviewers).

2. Profile likelihood phi not correctly fixed during optimization (rw.sd omits phi, but parameter initialization via c() concatenation may override profile-grid values). Raised by Alex, Charlie, Doug, and Evan. **Universal (4 of 4).**

3. No model diagnostics (ESS, conditional log-likelihood, simulation comparison). Raised by Alex, Charlie, Doug, and Evan. **Universal (4 of 4).**

4. ACF of returns incorrectly used to claim independence (squared returns not checked for ARCH effects). Raised by Alex, Charlie, Doug, and Evan. **Universal (4 of 4).**

5. Profile uses nprof=2 restarts per grid point, too sparse for reliable constrained optimization. Raised by Alex, Charlie, Doug, and Evan. **Universal (4 of 4).**

**Count of strictly universal AI-only flags (all 4 reviewers): 4** (items 2–5 above; item 1 is 3 of 4).
