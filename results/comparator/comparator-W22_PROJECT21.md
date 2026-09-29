# Comparator Analysis — W22 Project 21

---

## Human Issues

1. ARMA(4,4) is on the limit of the range of considered ARMA models, so if it seems the best then should one look further? In practice, ARMA(4,4) is already a complicated model.

2. It appears the fitted ARMA(4,4) is not doing a good job of explaining weekly periodicity. Perhaps sum cases over weeks to avoid this issue.

3. Raw R output can be hard to read and should be avoided. For example, `avg_7` is undefined in the EDA section. Labels and captions for figures would help the reader.

4. Population models are typically close to log-linear, so ARMA modeling is preferred on the log scale.

5. Setting $I_0=1$ is wildly implausible here, as you can see from the simulations struggling at the start of the pandemic. Perhaps one has to start a bit later (say, April) with higher $I_0$. Perhaps there were reporting rate issues right at the start, with a higher rate of undiagnosed cases.

6. Looking into the code, we find that the authors fixed the parameters $\mu_{IR}$, $\mu_{EI}$ and $\tau$. This needs more explanation and justification.

7. The delta wave model also has problems with its initial conditions.

8. The ARMA analysis is disconnected to the mechanistic modeling. ARMA is fitted with the complete data while pomp model is fitted partially so it is inappropriate to compare the partial model with a full model if the authors plan to make comparison based on the log likelihood as a benchmark.

9. The iterated filtering searches can get lost - especially evident for the delta variant. This can be due to model misspecification or a choice of random walk intensity which is much too large.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "ARMA applied to non-stationary series without transformation" and also by finding: "no stationarity analysis precedes ARMA modeling")
- Human Issue #5: contradiction (AI says I=1 is "a common convention... plausible but not justified"; human says I_0=1 is "wildly implausible")
- Human Issue #6: covered (matched by finding: "tau unused in dmeas/rmeas despite appearing in paramnames" and also by finding: "mu_EI and mu_IR fixed throughout pre-Delta local search")
- Human Issue #7: covered (matched by finding: "vaccination compartment initialization numerically negligible for Delta and Omicron")
- Human Issue #8: covered (matched by finding: "no comparison of log-likelihoods across segments or to any null model")
- Human Issue #9: missed

**Findings classification:**
- Finding 1 (measurement model SD=mean, CV=1): A — measurement model uses sqrt(mean^2)=mean as SD; tau never appears in dmeas/rmeas
- Finding 2 (tau completely unused): B — tau declared and log-transformed but never used in dmeas, rmeas, or rprocess (matches Human Issue #6)
- Finding 3 (vaccination compartment initialization wrong): B — Delta V initialized to 0.3% of N instead of ~31%; Omicron V initialized to difference of two vaccination rates (~0.1%) instead of cumulative ~59% (matches Human Issue #7)
- Finding 4 (mu_EI and mu_IR fixed in pre-Delta local search): B — rw.sd for pre-Delta perturbs only Beta, rho, eta; mu_EI and mu_IR held fixed throughout (matches Human Issue #6)
- Finding 5 (pre-Delta global search uses only 10 starting points): A — 10 starts for the longest, most complex segment vs. 20 for Delta and Omicron
- Finding 6 (ARMA applied to non-stationary series without transformation): B — raw undifferenced daily counts spanning three waves fitted to ARMA with no log transformation or differencing (matches Human Issue #4)
- Finding 7 (no profile likelihood or confidence intervals): A — no profile likelihoods computed for any parameter across any of the three models
- Finding 8 (SE filter threshold of 8 too permissive for pre-Delta): C — loglik.se < 8 filter is far too loose; Omicron uses 0.5 by comparison
- Finding 9 (Delta local search Np=2000): C — only 5 replicates at Np=2000 for Delta evaluation, vs. Np=20000 for pre-Delta
- Finding 10 (no log-likelihood comparison across segments or to null): D — three POMP log-likelihoods reported in isolation with no per-observation normalization or ARMA benchmark comparison (matches Human Issue #8)
- Finding 11 (pairs plot mixes local and global search without labeling): C — bind_rows combines both search types with no color-coding or faceting
- Finding 12 (rmeas/dmeas inconsistency in SD formula): C — rmeas uses sqrt(rho*H) as SD; dmeas uses rho*H as SD
- Finding 13 (initial pfilter uses only Np=100): C — Np=100 too small for hundreds of observations; yields unreliable initial log-likelihood
- Finding 14 (no stationarity analysis precedes ARMA modeling): D — ARMA section jumps to AIC table without ACF/PACF, unit root tests, or stationarity discussion (matches Human Issue #4)
- Finding 15 (pre-Delta E=0, I=1 initial condition): F — AI calls I=1 "a common convention... plausible but not justified"; human says I_0=1 is "wildly implausible" (contradicts Human Issue #5)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 4 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 1 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "ARMA model applied to non-stationary, non-homogeneous full-dataset without transformation")
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "tau declared in paramnames but never used in any Csnippet"; also matched by finding: "local search for pre-Delta locks mu_EI and mu_IR by omitting them from rw.sd")
- Human Issue #7: covered (matched by finding: "initial conditions do not conserve population in either SEIRV model")
- Human Issue #8: covered (matched by finding: "no benchmark comparison for ARMA vs. POMP models")
- Human Issue #9: covered (matched by finding: "no convergence diagnostics presented for global search")

**Findings classification:**
- Finding 1 (inconsistent sd between dmeasure and rmeasure): A — all three models score likelihood against wrong observation density
- Finding 2 (vaccination rate formula wrong by factor of N): A — alpha/N makes daily vaccination rate biologically incoherent
- Finding 3 (initial conditions do not conserve population in SEIRV models): B — Delta and Omicron initialization errors distort population sizes (matches Human Issue #7)
- Finding 4 (no profile likelihoods computed for any model): A — no basis for parameter identifiability or confidence intervals
- Finding 5 (pre-Delta global search: only 10 replicates and large Monte Carlo SE): A — insufficient computational effort for pre-Delta segment
- Finding 6 (tau declared in paramnames but never used in any Csnippet): B — tau is a phantom parameter occupying a free optimization dimension (matches Human Issue #6)
- Finding 7 (no benchmark comparison for ARMA vs. POMP models): B — ARMA fit to full data, POMP to sub-segments, no segment-level comparison attempted (matches Human Issue #8)
- Finding 8 (no convergence diagnostics presented for global search): B — no global search trace plots; Delta runs show divergence suggesting inadequate exploration (matches Human Issue #9)
- Finding 9 (dmeasure normal approximation can produce negative support): C — small rho*H values assign non-negligible probability to negative counts
- Finding 10 (local search for pre-Delta uses very small rw.sd and omits mu_EI, mu_IR): D — effectively fixes mu_EI and mu_IR at initial values throughout local search (matches Human Issue #6)
- Finding 11 (Delta local search uses Np=2000 with only 5 pfilter evaluations): C — inconsistent evaluation quality between local and global searches
- Finding 12 (global search box for pre-Delta is very narrow): C — box restricts search to small neighborhood of initial guess
- Finding 13 (ARMA model applied to non-stationary, non-homogeneous full-dataset): D — no log transform or differencing despite heterogeneous variance and multiple waves (matches Human Issue #4)
- Finding 14 (Omicron sigma values not compared to external vaccine effectiveness estimates): C — biological plausibility of sigma 0.27–0.62 not discussed
- Finding 15 (no model diagnostics beyond forward simulation): C — no conditional log-likelihood plots, ESS monitoring, or filtering distributions

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 4 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "Tau parameter declared but never used in any model — ghost parameter with no effect on model dynamics")
- Human Issue #7: covered (matched by finding: "Vaccinated compartment initialization incorrectly scaled for Delta and Omicron models")
- Human Issue #8: covered (matched by finding: "ARMA benchmark not quantitatively comparable to POMP log-likelihoods — different observation models, data lengths, and series coverage")
- Human Issue #9: covered (matched by finding: "Convergence traces for local search not described or interpreted; no-decrease in parameter variance is evidence of non-convergence")

**Findings classification:**
- Major #1 (dmeas/rmeas SD mismatch): A — dmeasure uses SD = mean_cases while rmeasure uses SD = sqrt(mean_cases), a ~500x discrepancy at peak counts, invalidating all likelihoods and parameter estimates
- Major #2 (vaccinated compartment init scaled incorrectly): B — Delta model initializes V at ~900,000 instead of ~93 million; Omicron uses only the incremental vaccination rate change rather than the total stock (matches Human Issue #7)
- Major #3 (smoothed observations in measurement model): A — 7-day rolling average introduces autocorrelation that violates the conditional independence assumption of the factored POMP likelihood
- Major #4 (no profile likelihoods): A — no profile likelihoods or confidence intervals computed for any of the three models despite 7–9 free parameters and known collinearity risks
- Major #5 (no model diagnostics): A — no conditional log-likelihood plots, no ESS reported, no filtering distribution shown; alignment problems with Delta and Omicron acknowledged but undiagnosed
- Major #6 (ARMA benchmark not comparable to POMP): B — ARMA fit to full series under Gaussian model while POMP models fit to sub-series; no common metric computed (matches Human Issue #8)
- Major #7 (tau declared but never used): B — tau in paramnames and perturbed by rw.sd in IF2 but never appears in rprocess or measurement Csnippets; ghost parameter wasting computational degrees of freedom (matches Human Issue #6)
- Major #8 (accumulator H tracks recoveries not infections): A — H += dN_IR accumulates recoveries but observed data records new confirmed cases; rho absorbs the ratio, becoming biologically uninterpretable
- Minor (rw.sd very small for pre-Delta): C — local search perturbs Beta by ~0.015% per step on natural scale; effective exploration likely very limited
- Minor (only 10 replicates for pre-Delta global search): C — 10 replicates provides very sparse coverage of 7-dimensional parameter box; models 2 and 3 use 20
- Minor (convergence traces not interpreted): D — traces plotted but not interpreted; authors note loglik plots are sparse without diagnosing non-convergence (matches Human Issue #9)
- Minor (loglik.se < 8 threshold permissive): C — model 1 pairs plot retains entries with SE up to 8 log-likelihood units while models 2 and 3 use 5 and 0.5 respectively
- Minor (alpha/N vaccination rate dimensionally inconsistent): C — dN_SV uses rbinom(S, 1 - exp(-alpha/N * dt)) producing essentially zero vaccinations per step; alpha should not be divided by N
- Minor (Omicron R initialization may be negative): C — R computed as residual absorbing ~270 million individuals under extreme assumption that ~90% of US population already recovered by December 2021
- Minor (no quantitative goodness-of-fit summary): C — reported log-likelihoods not interpreted relative to any null or benchmark, and number of observations not stated
- Minor (ARMA fit ignores structural breaks): C — single ARMA(4,4) applied to series spanning three qualitatively different dynamic regimes violates stationarity assumption

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "22.21.7 — ARMA ACF shows significant residual structure at lag 7 (weekly seasonality)")
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "22.21.7 — recommends log-transformation before ARMA fitting")
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "22.21.6 — tau declared but absent from dmeas/rmeas, non-functional in likelihood"; also matched by finding: "22.21.15 — mu_IR and mu_EI not perturbed in pre-Delta local search")
- Human Issue #7: missed
- Human Issue #8: covered (matched by finding: "22.21.13 — ARMA benchmark fitted to full series while POMP models fitted to sub-segments, making comparison inconsistent")
- Human Issue #9: covered (matched by finding: "22.21.4 — pre-Delta optimization not converged, chains spread over ~2500 log-likelihood units"; also matched by finding: "22.21.11 — Delta segment shows strong non-identifiability with diffuse parameter clouds, not discussed")

**Findings classification:**
- 22.21.1: A — measurement model degenerate and internally inconsistent (dmeas and rmeas implement different distributions)
- 22.21.6: B — tau declared and log-transformed but absent from dmeas/rmeas in all three models, making it non-identifiable (matches Human Issue #6)
- 22.21.9: A — Omicron model initializes vaccinated compartment V using one-day vaccination change rather than cumulative fraction, off by factor ~600
- 22.21.2: A — no profile likelihoods or confidence intervals computed for any parameter across all three segments
- 22.21.3: A — ARMA(4,4) benchmark presented but no quantitative likelihood comparison to POMP models is made
- 22.21.4: B — pre-Delta local search trace shows declining log-likelihoods and chains spread over ~2500 log-likelihood units; optimization has not converged (matches Human Issue #9)
- M1: A — estimated parameters are biologically implausible (mu_IR=0.86 implying ~1.2-day infectious period; rho≈1 implying ~100% reporting rate) and this is not discussed
- 22.21.15: D — mu_IR and mu_EI not perturbed in pre-Delta local search rw.sd, remaining fixed at starting values across all chains (matches Human Issue #6)
- 22.21.7: D — ARMA fitted to raw counts without log-transformation; ACF of residuals shows significant structure at lag 7 (weekly seasonality) (matches Human Issues #2 and #4)
- 22.21.10: C — no filtering diagnostics (conditional log-likelihood per time step, ESS) shown for any segment
- 22.21.11: D — Delta segment global and local optima differ dramatically and pairs plot shows diffuse parameter clouds; strong non-identifiability not discussed (matches Human Issue #9)
- 22.21.13: D — ARMA benchmark fitted to full 800+ day series while POMP models fitted to sub-segments, making comparison inconsistent (matches Human Issue #8)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 1 |
| D (AI minor, human also found) | 4 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 3 | 4 | 5 | 5 |
| B (AI major, human also found) | 4 | 4 | 3 | 2 |
| C (AI minor, human missed) | 5 | 5 | 7 | 1 |
| D (AI minor, human also found) | 2 | 2 | 1 | 4 |
| E (Human found, AI missed) | 4 | 4 | 5 | 4 |
| F (Human-AI contradiction) | 1 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 4 | 2 | 4 | 4/8 = 50% | 3 | 5 | 8/14 = 57% |
| Charlie | 4 | 2 | 4 | 5/9 = 56% | 4 | 5 | 9/15 = 60% |
| Doug | 3 | 1 | 5 | 4/9 = 44% | 5 | 7 | 12/16 = 75% |
| Evan | 2 | 4 | 4 | 5/9 = 56% | 5 | 1 | 6/12 = 50% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #1: ARMA(4,4) is on the limit of the range of considered ARMA models, so if it seems the best then should one look further? In practice, ARMA(4,4) is already a complicated model. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #3: Raw R output can be hard to read and should be avoided. For example, `avg_7` is undefined in the EDA section. Labels and captions for figures would help the reader. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 2 out of 9 human issues (22%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #2: It appears the fitted ARMA(4,4) is not doing a good job of explaining weekly periodicity. Perhaps sum cases over weeks to avoid this issue. (Covered only by Evan)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 1 |
