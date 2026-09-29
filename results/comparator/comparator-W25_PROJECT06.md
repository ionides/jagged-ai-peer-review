# Comparator Analysis — W25 Project 06

---

## Human Issues

1. Too little time was spent on the mechanistic POMP model compared to ARMA and deep learning. The difficulties experienced with the postulated POMP model need thoughtful diagnostics to figure out how to make both the science and the time series data analysis work together coherently.

2. MAPE is not comparable between data transformations (for the same reason log-likelihood is not), yet the team uses it to assess methods across different data transformations without proper adjustment. Using elaborate modern methods (VMD, N-BEATS) should not come at the expense of complete and careful use of the appropriate methods studied in class.

3. Likelihood is a more efficient inference metric than MAPE; if the team preferred MAPE, they should have calculated MAPE also for the SEIR model to allow a fair comparison.

4. The ADF test is inappropriate and a poor choice here. The peaks are visibly diminishing through time, indicating nonstationarity; the ADF model is especially inappropriate before taking logs and remains a poor choice even after.

5. The claim that "the residual time series plot shows no visible trend or seasonal structure" for ARMA is incorrect. The time plot of residuals shows extreme heteroskedasticity matching seasonal peaks and troughs, which is a diagnostic signal that a logarithmic transformation should be considered.

6. The SEIR model is not compared to the ARMA benchmark. The fitted SEIR model falls short of ARMA by 157 log-likelihood units (3760 vs. 3603), a large discrepancy suggesting the SEIR model is missing something important.

7. Particle depletion, numerical overflow, and degeneracy in measurement likelihoods during inference are typical signs of a poor model fit. The inflexible modeling of seasonality or the lack of overdispersion in the process model may be the issue; diagnostic checks for the POMP model would help track this down.

8. Mean/median summary statistics are not meaningful for a time series with substantial dynamic variation; presenting them and making statements about symmetry is appropriate only when data are well modeled as i.i.d.

9. For comparing ARMA with log-ARMA, a Jacobian calculation should be used to put the log-likelihood and AIC values on the same scale (as in the measles case study, Chapter 18).

10. Examining ACF, PACF, and Box-Ljung statistics for residuals of a large ARMA selected by AIC is almost always uninformative; it would be better to examine normality of residuals, which would reveal long tails and provide another clue that a log transform is appropriate.

11. The Outlook section appears to be produced by GenAI: it lists modern methods without references or details, and the generic assertions are the kind of content GenAI could generate.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "loglik.se filter threshold of 10 too permissive; several runs show substantial particle-filter instability")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed
- Human Issue #11: missed

**Findings classification:**
- Finding 1 (NewEI accumulates wrong compartment): A — code bug causes systematic undercount of weekly incidence; not raised by human
- Finding 2 (emeas uses monotonically growing H): A — inconsistency between emeas and dmeas/rmeas; not raised by human
- Finding 3 (SEIRS mislabeled as SEIR throughout): A — waning immunity term present in code but not acknowledged; not raised by human
- Finding 4 (population N = 2267000 incorrect for national model): A — underestimated N inflates transmission estimates; not raised by human
- Finding 5 (amp unconstrained in local mif2 call): A — constraint omitted from partrans, amp > 1 in results; not raised by human
- Finding 6 (written equations include terms absent from code): A — birth, death, importation terms documented but not implemented; not raised by human
- Finding 7 (profile likelihood is a marginal scatter plot): A — wrong method and wrong chi-square threshold used; not raised by human
- Finding 8 (cross-model comparison information asymmetry): A — NBEATS uses county-level features, ARMA/POMP use national aggregate; not raised by human
- Finding 9 (VMD fit on full dataset including validation period): A — data leakage inflates NBEATS MAPE; not raised by human
- Finding 10 (ARMA ignores 52-week seasonality): C — no SARIMA considered; not raised by human
- Finding 11 (ARMA MAPE evaluated in-sample only): C — in-sample vs. validation MAPE comparison inconsistency; not raised by human
- Finding 12 (loglik.se < 10 filter too permissive): D — retained runs with high SE indicate particle-filter instability (matches Human Issue #7)
- Finding 13 (start_params undefined in local search code): C — implicit parameter source, reproducibility concern; not raised by human
- Finding 14 (duplicate library(pomp) call): C — cosmetic error, not raised by human
- Finding 15 (Beta range 83–748 implausibly wide, unexplained): C — likely artifact of confounded N and unconstrained amp; not raised by human

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 9 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 10 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "Log-ARMA vs. linear-ARMA MAPE comparison is not valid — MAPE on log scale and raw scale have no common interpretation")
- Human Issue #3: covered (matched by finding: "Three-model comparison uses incompatible metrics and data — POMP is never assigned a MAPE or out-of-sample metric")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "POMP model substantially underperforms ARMA benchmark by ~156 log-lik units with no acknowledgment")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: covered (matched by finding: "Log-ARMA vs. linear-ARMA MAPE comparison is not valid — MAPE on log scale and raw scale have no common interpretation")
- Human Issue #10: missed
- Human Issue #11: missed

**Findings classification:**
- Finding 1 (POMP underperforms ARMA by 156 log-lik units, unacknowledged): B — matches Human Issue #6
- Finding 2 (Profile likelihood for ρ is not a true profile; wrong Wilks cutoff): A — no human issue raised this
- Finding 3 (`ivp()` mis-applied to non-IVP parameters in `rw.sd`): A — no human issue raised this
- Finding 4 (Text model contradicts code — births, deaths, importation absent from implementation): A — no human issue raised this
- Finding 5 (Three-model comparison uses incompatible metrics and data): B — matches Human Issue #3
- Finding 6 (`emeas` uses cumulative H, inconsistent with `dmeas`/`rmeas` using NewEI): A — no human issue raised this
- Finding 7 (No SARIMA considered despite prominent 52-week seasonality): A — no human issue raised this
- Finding 8 (`omega` absent from `rw.sd` in global search): C — no human issue raised this
- Finding 9 (Profile CI degenerate under correct Wilks threshold): C — no human issue raised this
- Finding 10 (Cooling fraction 0.3 departs from course standard without justification): C — no human issue raised this
- Finding 11 (Initial SEIR parameter values biologically implausible for chickenpox): C — no human issue raised this
- Finding 12 (Log-ARMA vs. linear-ARMA MAPE comparison invalid): D — matches Human Issues #2 and #9
- Finding 13 (`loglik.se < 10` filter excessively permissive): C — no human issue raised this
- Finding 14 (Redundant/inconsistent `partrans` re-specified inside local search `mif2`): C — no human issue raised this
- Finding 15 (Duplicate `library(pomp)`; auto-install without consent): C — no human issue raised this

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "No benchmark comparison of POMP model against non-mechanistic baseline")
- Human Issue #7: covered (matched by finding: "Missing accumvars causes measurement model to use only last Euler sub-step"; also matched by finding: "Amplitude parameter amp estimated without transformation constraint, producing values exceeding 1")
- Human Issue #8: missed
- Human Issue #9: covered (matched by finding: "Log-ARMA and ARMA log-likelihoods described as not directly comparable but are compared by implication")
- Human Issue #10: missed
- Human Issue #11: missed

**Findings classification:**
- Major #1 (Missing accumvars): B — accumvars absent causes measurement model to see only 1/7 of weekly new-infection flow, producing near-zero likelihoods and particle depletion (matches Human Issue #7)
- Major #2 (Population N ≈ 22% of actual): A — N = 2267000 is roughly one-quarter of Hungary's true population, inflating effective Beta by a factor of ~4.4
- Major #3 (Global search anti-pattern): A — global search reuses mif2 result from local search, inheriting exhausted cooling schedule and thus failing to be genuinely global
- Major #4 (amp without transformation constraint): B — amp is estimated on the natural scale with no upper bound, producing values > 2.1 that imply complete seasonal cessation of transmission (matches Human Issue #7)
- Major #5 (Profile likelihood is pseudo-profile): A — "Poor Man's Profile" filters global-search scatter instead of running constrained optimization at each rho grid point; chi-squared cutoff uses −4 instead of −1.92
- Major #6 (No benchmark comparison): B — POMP and ARMA log-likelihoods are derived under different observation models and cannot be directly compared; no equivalent-observation-model baseline provided (matches Human Issue #6)
- Major #7 (ODE vs Csnippet discrepancy): A — equations include birth/death terms (mu*N, -mu*S) but the seir_step Csnippet contains no demographic flows; stated and implemented models do not match
- Minor (SEIR vs SEIRS mislabeling): C — model includes waning immunity (omega, dN_RS) making it SEIRS, but prose and section titles call it SEIR throughout
- Minor (Incorrect CI threshold): C — code uses maxloglik − 4 as CI cutoff; correct 95% threshold is maxloglik − 1.92
- Minor (amp upper bound in global search): C — runif_design sets amp upper bound at 0.4 but the logit constraint is not enforced, so mif2 freely moves amp above 0.4
- Minor (mu_IR lower bound implausible): C — lower bound of 0.03/week implies 33-week infectious period; chickenpox infectious period is ~5–7 days
- Minor (H accumulates recoveries): C — emeas Csnippet computes rho*H where H is a running cumulative total of I-to-R transitions since t=0, not a weekly count
- Minor (Deep learning evaluation incompletely described): C — train/validation/test split dates, epochs, and hyperparameter selection not reported; MAPE figures cannot be interpreted relative to ARMA
- Minor (Duplicate library(pomp)): C — setup chunk loads library(pomp) twice, indicating copy-paste editing without cleanup
- Minor (Auto-installing packages): C — POMP setup chunk calls install.packages() during rendering without user consent
- Minor (plan(multicore) portability): C — plan(multicore) is unsupported on Windows; plan(multisession) would be more portable
- Minor (Log-ARMA/ARMA log-likelihoods incomparability): D — paper acknowledges log-ARMA AIC and linear ARMA AIC are not directly comparable due to data scale change, then contrasts them anyway; Jacobian adjustment needed (matches Human Issue #9)
- Minor (Population size not justified): C — N = 2267000 stated without citation or explanation of which catchment population it represents

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 10 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "25.06.M7 — no common evaluation framework; MAPE values across methods use different splits, horizons, and inputs, making comparison invalid")
- Human Issue #3: covered (matched by finding: "25.06.M7 — POMP shown only visually without a metric, no fair basis for comparative claims")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "25.06.M1 — best POMP log-likelihood not extracted or compared to ARMA loglik of -3603.27")
- Human Issue #7: covered (matched by finding: "25.06.NEW-B — ESS monitoring absent; cannot assess particle degeneracy quality")
- Human Issue #8: missed
- Human Issue #9: contradiction (Evan's S5 says authors correctly handled AIC comparability by noting the incomparability; human says a Jacobian calculation is needed to actually put log-likelihoods on the same scale)
- Human Issue #10: missed
- Human Issue #11: missed

**Findings classification:**
- 25.06.M2: A — Profile likelihood for rho is invalid and CI threshold (maxloglik - 4) is too lenient; should be maxloglik - 1.92
- 25.06.M5: A — amp parameter does not converge across all 20 local search chains, not acknowledged in text
- 25.06.NEW-A: A — Fitted mu_EI (0.13–0.16/week) is biologically implausible for chickenpox; not discussed
- 25.06.M9: A — Lambda importation term appears in mathematical formulation but is absent from the Csnippet code
- 25.06.M4: C — No seasonal ARMA component despite clear 52-week periodicity in the data
- 25.06.M3: C — ARMA residual ACF x-axis shows normalized units (0 to 1.0) rather than lag weeks
- 25.06.M7: D — No common evaluation framework across the three methods; incomparable MAPE values, splits, horizons, and data inputs (matches Human Issues #2 and #3)
- 25.06.M1: D — Best POMP log-likelihood not reported in text or compared to ARMA benchmark (matches Human Issue #6)
- 25.06.NEW-B: D — ESS monitoring absent; cannot diagnose particle degeneracy (matches Human Issue #7)
- 25.06.M12: C — Model includes waning immunity making it SEIRS, but consistently called SEIR throughout
- 25.06.M6b: C — loglik.se filter threshold of 10 is too loose relative to standard practice of < 1
- S5 (strength note): F — Evan says authors "correctly" handled AIC comparability by noting incomparability of log vs original scale; human says a Jacobian calculation is required to actually put the values on the same scale (contradicts Human Issue #9)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 3 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 1 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 9 | 5 | 4 | 4 |
| B (AI major, human also found) | 0 | 2 | 3 | 0 |
| C (AI minor, human missed) | 5 | 7 | 10 | 4 |
| D (AI minor, human also found) | 1 | 1 | 1 | 3 |
| E (Human found, AI missed) | 10 | 7 | 8 | 6 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 1 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 0 | 1 | 10 | 1/11 = 9% | 9 | 5 | 14/15 = 93% |
| Charlie | 2 | 1 | 7 | 4/11 = 36% | 5 | 7 | 12/15 = 80% |
| Doug | 3 | 1 | 8 | 3/11 = 27% | 4 | 10 | 14/18 = 78% |
| Evan | 0 | 3 | 6 | 4/10 = 40% | 4 | 4 | 8/11 = 73% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #1: Too little time was spent on the mechanistic POMP model compared to ARMA and deep learning. The difficulties experienced with the postulated POMP model need thoughtful diagnostics to figure out how to make both the science and the time series data analysis work together coherently. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #4: The ADF test is inappropriate and a poor choice here. The peaks are visibly diminishing through time, indicating nonstationarity; the ADF model is especially inappropriate before taking logs and remains a poor choice even after. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #5: The claim that "the residual time series plot shows no visible trend or seasonal structure" for ARMA is incorrect. The time plot of residuals shows extreme heteroskedasticity matching seasonal peaks and troughs, which is a diagnostic signal that a logarithmic transformation should be considered. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #8: Mean/median summary statistics are not meaningful for a time series with substantial dynamic variation; presenting them and making statements about symmetry is appropriate only when data are well modeled as i.i.d. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #10: Examining ACF, PACF, and Box-Ljung statistics for residuals of a large ARMA selected by AIC is almost always uninformative; it would be better to examine normality of residuals, which would reveal long tails and provide another clue that a log transform is appropriate. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #11: The Outlook section appears to be produced by GenAI: it lists modern methods without references or details, and the generic assertions are the kind of content GenAI could generate. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 6 out of 11 human issues (55%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

(none)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |
