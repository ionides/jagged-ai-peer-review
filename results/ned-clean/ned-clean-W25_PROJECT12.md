# Ned-Clean Analysis — W25 Project 12

---

## Human Issues

1. The ADF test is not appropriate to examine non-stationary variance (Section 2.2).
2. ARMA is described as modeling "key autocorrelation patterns" but the sample ACF and AIC table show there are no evident autocorrelation patterns — the characterization is misleading.
3. The likelihood values are quite close; it would be worth verifying whether the GARCH likelihood is actually a likelihood and not a conditional likelihood of some kind.
4. There is a missed opportunity to use the POMP framework's flexibility to improve the return distribution model (e.g., adding a t-distribution to the measurement model).
5. The regime-switching model attempt does not help much, and modeling longer tails is noted as more important — the POMP novelty did not deliver meaningful improvement.
6. The ACF of squared residuals is described as not showing significant spikes after lag 1, but this potentially informative plot is never shown.
7. The SV log-likelihood is stated as higher than ARIMA and GARCH benchmarks, but this is only true except for the t-distributed GARCH model — suggesting a t-distribution should be added to the SV model.
8. The GARCH AIC values in Table 3 are not mathematically consistent; the consequences of imperfect maximization should be discussed.
9. The Table 3 lowest AIC value referenced in the text (-5046.13) does not appear in the table.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: covered (matched by finding #10: "GARCH AIC table description inconsistency — text cites -5046.13 as lowest AIC")

**Findings classification:**
- Finding #1 (negative Heston sigma/v0): A — physically impossible Heston parameter estimates dismissed without justification
- Finding #2 (no AIC/BIC for POMP): A — likelihood comparison not penalized for parameter count
- Finding #3 (ARMA order inconsistency in GARCH code vs stated model): A — inconsistency between stated ARMA order and code labels
- Finding #4 (kappa not fixed properly in rw.sd): A — profile likelihood for Heston does not fix kappa in rw.sd
- Finding #5 (single pfilter per replicate): A — only a single particle filter evaluation per replicate for likelihood scoring
- Finding #6 (data extends beyond stated analysis period): A — data file contains observations past stated end date
- Finding #7 (regime trajectory from simulate() not filtering): A — regime-switching plot based on single simulation not filtered states
- Finding #8 (no CIs for profile likelihoods): A — no confidence intervals or uncertainty quantification for profile likelihoods
- Finding #9 (figure numbering inconsistent): C — inconsistent figure numbering (duplicate Figure 3)
- Finding #10 (GARCH AIC table inconsistency): D — GARCH AIC table description cites -5046.13 and inconsistent selection justification (matches Human Issue #9)
- Finding #11 (hardcoded LL values in Table 5): C — log-likelihood values in Table 5 are hardcoded rather than computed at runtime
- Finding #12 (no ESS diagnostics): C — no effective sample size diagnostics reported
- Finding #13 (prior course projects cited as literature): C — discussion references prior course projects as if published studies
- Finding #14 (Heston lacks leverage effect): C — Heston model lacks a leverage effect despite discussion of asymmetry
- Finding #15 (typos): C — typos and language issues including misspelling in section header

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: covered (matched by finding #11: "GARCH AIC values in Table 3 inconsistent with those cited in text")
- Human Issue #9: missed

**Findings classification:**
- Finding #1 (regime plot uses simulate() not filtering): A — regime-switching latent state plot uses forward simulation rather than filtering distribution
- Finding #2 (profile: single restart, single pfilter, no CIs): A — profile likelihoods use single IF2 restart and single particle filter evaluation with no confidence intervals
- Finding #3 (negative Heston sigma/v0 dismissed): A — negative sigma and v0 in Heston MLE dismissed without model-misspecification consideration
- Finding #4 (LL comparison not AIC-adjusted): A — log-likelihood comparison across model families is not AIC-adjusted
- Finding #5 (no non-mechanistic benchmark for POMP): A — no benchmark comparison of POMP models against non-mechanistic alternatives
- Finding #6 (profile evaluated on wrong model object): A — Heston profile likelihood evaluated against heston_model rather than constrained model object
- Finding #7 (ARIMA/POMP LL comparability issue): C — log-likelihood comparison between ARIMA and POMP requires identical observation models and data
- Finding #8 (2025 hold-out claimed but not performed): C — discussion references a common 2025 hold-out but no out-of-sample evaluation is performed
- Finding #9 (ESS not monitored): C — effective sample size not monitored; particle degeneracy cannot be ruled out
- Finding #10 (p11 near 0.5 near-random switching): C — RS transition probability p11 ≈ 0.52 implies near-random switching, not persistence
- Finding #11 (GARCH AIC Table 3 inconsistency): D — GARCH AIC values in Table 3 inconsistent with mathematical implications of reported log-likelihoods (matches Human Issue #8)
- Finding #12 (figure numbering collision): C — two figures labeled "Figure 3"
- Finding #13 (rw.sd magnitude for mu): C — rw.sd for mu equals starting value (100% perturbation), too large
- Finding #14 (no model diagnostics beyond traces/QQ): C — no simulated trajectory overlays, conditional log-likelihoods, or summary-statistic comparisons
- Finding #15 (typos and terminology): C — Section 2.2 "Stationairty" misspelling; ARMA(1,1) vs ARMA(2,2) inconsistency; "AMIRA" typo

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: covered (matched by finding #15: "ADF test interpretation — paper uses only ADF, should also apply KPSS")
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding #1: "invalid direct comparison — GARCH LLH is not the marginal likelihood of the observation series")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed

**Findings classification:**
- Finding #1 (invalid LL comparison across families): B — GARCH and ARIMA log-likelihoods are not on the same scale; GARCH LLH is not the marginal likelihood (matches Human Issue #3)
- Finding #2 (negative Heston sigma/v0): A — negative estimates for sigma and v0 dismissed; no parameter transformations imposed
- Finding #3 (profile single restart/pfilter, no CI): A — profile uses single restart and single pfilter evaluation; no confidence interval derived
- Finding #4 (regime plot uses simulation): A — regime sequence plot uses forward simulation not filtering distribution
- Finding #5 (no non-mechanistic benchmark): A — no proper non-mechanistic benchmark for POMP models
- Finding #6 (p11 near 0.5 near-random): A — RS transition probability p11 ≈ 0.52 implies near-random regime switching, not persistence
- Finding #7 (figure numbering inconsistent): C — figure numbering inconsistent, duplicate "Figure 3"
- Finding #8 (ARIMA mean spec inconsistency): C — inconsistency between ARMA(2,2), ARMA(1,1), and ARMA(2,0,2) descriptions across sections
- Finding #9 (RS global search rw.sd reuses local-search object): C — RS global search rw.sd magnitudes too small relative to initialization box width
- Finding #10 (ESS claimed monitored but no plot shown): C — ESS trajectories claimed as monitored but no ESS plot or numerical summary provided
- Finding #11 (pfilter called on wrong object in Heston profile): C — Heston profile pfilter called on heston_model not constrained object
- Finding #12 (no model diagnostics): C — no conditional log-likelihood plots, simulated trajectory overlays, or summary-statistic comparisons
- Finding #13 (no parameter transformations for Heston): C — sigma and v0 not constrained positive; no partrans argument
- Finding #14 (MLE parameter vectors not archived): C — final MLE parameter vectors not archived; reproducibility requires full re-run
- Finding #15 (ADF test interpretation): D — paper uses only ADF test; stationarity conclusion is one-sided without KPSS corroboration (matches Human Issue #1)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed

**Findings classification:**
- 25.12.1 (Heston negative parameters): A — physically impossible Heston parameter estimates (sigma < 0, v0 < 0)
- 25.12.2 (ARIMA AIC inconsistency): A — AIC value for ARIMA(2,0,2) stated in text is inconsistent with table and log-likelihood
- 25.12.3 (GARCH mislabeled in final comparison): A — Table 5 labels GARCH(1,3) but Section 4 selects GARCH(1,1) after diagnostics
- 25.12.4 (kappa profile no lower CI bound): A — kappa profile flat from 0.7–1.7, optimum at left edge, lower bound cannot be determined
- 25.12.5 (sigma_2 profile numerically unstable): A — sigma_2 profile shows two local maxima with valley; unreliable for CI derivation
- 25.12.6 (logit inversion error, near-random regime switching): A — logit inversion error yields p11 ≈ 0.44 not 0.52; near-random regime switching
- 25.12.7 (ESS not monitored): A — ESS not monitored or reported despite text claiming it was
- 25.12.8 (no CIs for any parameter): A — no confidence intervals reported for any model parameter
- 25.12.M3 (predictive accuracy promised but not delivered): A — Introduction promises out-of-sample evaluation but only in-sample results are presented
- 25.12.11 (pfilter replication count unspecified): C — number of pfilter replicates not reported; logmeanexp vs max not confirmed
- 25.12.10 (convergence to invalid region not flagged): C — trace plots showing convergence to sigma ≈ 0 and v0 < 0 described as "strong convergence" without noting constraint violation
- 25.12.12 (ARMA order inconsistency in text): C — ARMA(2,2) selected in Section 3 but Section 4 refers at two points to ARMA(1,1)+GARCH(1,1)
- Notation/presentation: C — LaTeX rendering error in GARCH-t equation; figure numbering inconsistent; Wikipedia reference; y-axis label cut off

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 9 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 9 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 8 | 6 | 5 | 9 |
| B (AI major, human also found) | 0 | 0 | 1 | 0 |
| C (AI minor, human missed) | 6 | 8 | 8 | 4 |
| D (AI minor, human also found) | 1 | 1 | 1 | 0 |
| E (Human found, AI missed) | 8 | 8 | 7 | 9 |

---

## Per-Reviewer Metrics

Human Recall = (B + D) / (B + D + E)
AI-Unique Rate = (A + C) / (A + B + C + D)

| Reviewer | B | D | E | Human Recall | A | C | AI-Unique Rate |
|----------|--:|--:|--:|-------------:|--:|--:|---------------:|
| Alex | 0 | 1 | 8 | 1/9 = 11.1% | 8 | 6 | 14/15 = 93.3% |
| Charlie | 0 | 1 | 8 | 1/9 = 11.1% | 6 | 8 | 14/15 = 93.3% |
| Doug | 1 | 1 | 7 | 2/9 = 22.2% | 5 | 8 | 13/15 = 86.7% |
| Evan | 0 | 0 | 9 | 0/9 = 0.0% | 9 | 4 | 13/13 = 100.0% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer (Alex, Charlie, Doug, Evan) failed to cover:

- Human Issue #2: ARMA described as modeling "key autocorrelation patterns" but ACF and AIC table show no evident patterns — misleading characterization.
- Human Issue #4: Missed opportunity to add t-distribution to POMP measurement model.
- Human Issue #5: Switching model attempt does not help much; longer tails more important — POMP novelty did not deliver.
- Human Issue #6: ACF of squared residuals described as uninformative but this potentially informative plot is never shown.
- Human Issue #7: SV log-likelihood stated as higher than all benchmarks, but t-GARCH exceeds it — t-distribution should be added to SV model.

Total consensus misses: 5 out of 9 human issues (55.6%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #1 (ADF test): covered only by Doug (finding #15). Missed by Alex, Charlie, Evan.
- Human Issue #3 (GARCH likelihood nature): covered only by Doug (finding #1). Missed by Alex, Charlie, Evan.
- Human Issue #8 (GARCH AIC mathematically inconsistent): covered only by Charlie (finding #11). Missed by Alex, Doug, Evan.
- Human Issue #9 (Table 3 AIC -5046.13 not in table): covered only by Alex (finding #10). Missed by Charlie, Doug, Evan.

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 1 |
| Charlie | 1 |
| Doug | 2 |
| Evan | 0 |

### Universal AI-only flags

Issues raised as Major by every reviewer that the human did not mention:

- Negative/physically impossible Heston parameter estimates (sigma < 0, v0 < 0): raised as Major by Alex (#1), Charlie (#3), Doug (#2), Evan (#1).
- Profile likelihood uses single restart and single pfilter per grid point with no confidence interval derived: raised as Major by Alex (#8 and #4/5), Charlie (#2), Doug (#3), Evan (#4/#5/#8).
- Regime-switching "inferred" regime plot based on simulate() not particle filter: raised as Major by Alex (#7), Charlie (#1), Doug (#4), Evan (implicitly via 25.12.6 and broader pattern — actually Evan does not explicitly name simulate() as the error. Let me recheck.

Re-checking Evan for the simulate() finding: Evan's review does not include a finding explicitly flagging the use of simulate() for the regime plot. Evan #25.12.6 is about logit inversion error and near-random regime switching. The simulate()-as-latent-inference error is not a named finding in Evan's review.

Revised universal AI-only flags (raised as Major by all four reviewers):

- Negative Heston parameter estimates: raised as Major by Alex (#1), Charlie (#3), Doug (#2), Evan (25.12.1). Count: 4/4 reviewers.
- Profile likelihoods have insufficient restarts and no confidence intervals: raised as Major by Alex (#4, #5, #8), Charlie (#2), Doug (#3), Evan (25.12.4, 25.12.5, 25.12.8). Count: 4/4 reviewers.

Issues raised as Major by three of four reviewers:

- Regime sequence plot uses simulate() not filtering distribution: Alex (#7), Charlie (#1), Doug (#4). Evan does not flag this explicitly. Count: 3/4 reviewers.
- Log-likelihood comparison not adjusted for parameter count / model families not comparable: Alex (#2), Charlie (#4), Doug (#1), Evan (25.12.3 — mislabeled GARCH specification, which is related but distinct). Count depends on interpretation; the core cross-model LL comparison concern is in Alex, Charlie, and Doug.

Universal AI-only flags (all four reviewers, Major): 2 issues.
- Physically impossible Heston parameter estimates (negative sigma, v0).
- Profile likelihood: single restart per grid point, single pfilter evaluation, no confidence interval computed.
