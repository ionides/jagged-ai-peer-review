# Comparator Analysis — W21 Project 11

---

## Human Issues

1. Section 2: What is the shaded region around the trend line? Is it meaningful in this situation?

2. This is a case where the Augmented Dickey-Fuller (ADF) test is not particularly appropriate, since the null hypothesis of an ARMA model is not of much interest.

3. Section 3. If you decide to test for stationarity with ADF or similar, and you conclude there is nonstationarity, then fitting a stationary model is not a natural next step.

4. Section 4. The POMP model implemented is not an ODE system, so it is best not to write it as one.

5. From the simulations, you can see that the variability in the data is much higher than the simulations, which follow a smooth curve with little stochasticity. This is the first of many warning signs about what is wrong with the model.

6. The perturbed model (with parameters having a random walk) obtains log likelihoods around -300. As the perturbations decrease, the likelihood goes down and filtering failures (large drops in the estimated likelihood) start occurring. This is most likely a result of insufficient process and/or measurement noise. All models use binomial measurement, which can be problematic partly because of the bounded support and partly because it cannot fit overdispersion. Similarly, no models included additional noise in the rates.

7. Effective sample size is often close to zero, which is another indication of insufficient stochasticity in the model. Modeling multiple COVID waves is not easy: see Projects 13 and 15 for successful approaches.

8. The project mentions the possibility of trying models with additional variability, but does not get around to doing it. For a 5-person group, some subset could have been delegated this task.

9. References should follow a standard format. Links are helpful, but one should be able to look through the reference list without clicking on each one.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "extremely poor log-likelihood values — model fit is catastrophically bad")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed

**Findings classification:**
- Finding 1 (H accumulator initialized to (1-eta)*N): A — H initialized incorrectly to (1-eta)*N instead of 0
- Finding 2 (measurement model links reports to I-to-R flow): A — binomial measurement model uses wrong transition (I-to-R instead of E-to-I)
- Finding 3 (no profile likelihood or confidence intervals): A — parameter uncertainty completely ignored, no profile likelihoods computed
- Finding 4 (catastrophically poor log-likelihood values): B — best log-likelihood ~-10,633 with no null model comparison (matches Human Issue #6)
- Finding 5 (logit transform on Beta invalid): A — logit constrains Beta to (0,1) when Beta can exceed 1
- Finding 6 (global search mif2 non-standard and underspecified): A — two sequential mif2 calls without proper rw.sd specification
- Finding 7 (external URL dependency breaks reproducibility): A — POMP section reads data from external GitHub URL
- Finding 8 (two different data streams for ARMA and POMP): C — raw vs. smoothed data used inconsistently across sections
- Finding 9 (HP filter lambda=100 inappropriate for daily data): C — lambda=100 designed for annual macroeconomic data, not daily epidemiological data
- Finding 10 (rho fixed at 0.1 without sensitivity analysis): C — reporting rate fixed with no sensitivity analysis or joint estimation
- Finding 11 (initial conditions E(0) and I(0) hard-coded): C — initial conditions never estimated or profiled
- Finding 12 (convergence diagnostics incomplete and misread): C — narrative written out of order, no geometric cooling fraction reported
- Finding 13 (ARMA model selection poorly justified): C — code fits ARMA(1,1) but text selects ARMA(2,2) without clear justification
- Finding 14 (weekly seasonality in residuals not addressed): C — seventh-lag ACF spike noted but no SARMA or day-of-week correction attempted
- Finding 15 (no simulation-based model check after fitting): C — no posterior predictive simulation from estimated parameters shown

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
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
- Human Issue #6: covered (matched by finding: "Very large Monte Carlo SEs / filtering failures confirm severe model misspecification / particle collapse")
- Human Issue #7: covered (matched by finding: "Very large Monte Carlo SEs / filtering failures confirm severe model misspecification / particle collapse")
- Human Issue #8: missed
- Human Issue #9: missed

**Findings classification:**
- Finding 1 (measurement model bug — H accumulates dN_IR instead of dN_EI): A — fundamental structural error in measurement model; human did not raise this specific bug
- Finding 2 (rho and eta fixed without estimation): A — reporting rate and susceptibility fraction fixed without likelihood-based justification; human did not raise this
- Finding 3 (no profile likelihoods): A — no profile likelihood computed for any parameter; human did not raise this
- Finding 4 (global search insufficient computational effort): A — Nmif=50, particle degeneracy, SE >> 1; human did not raise this
- Finding 5 (no non-mechanistic benchmark): A — POMP likelihood never compared to ARMA or other baseline; human did not raise this
- Finding 6 (very large Monte Carlo SEs in reported likelihoods): B — particle collapse and filtering failures confirming severe misspecification (matches Human Issues #6 and #7)
- Finding 7 (H initialized to N*(1-eta) instead of zero): A — initialization inconsistency; human did not raise this
- Finding 8 (ARMA model selection text contradicts code — arima11 printed instead of arima22): A — text-code inconsistency in ARMA selection; human did not raise this
- Finding 9 (rw.sd magnitudes too small for logit-transformed parameters): C — minor; human did not raise this
- Finding 10 (HP filter lambda=100 inappropriate for daily data): C — minor; human did not raise this
- Finding 11 (convergence diagnosis focuses on parameter spread rather than loglik stability): C — minor; human did not raise this
- Finding 12 (global search description appears before the code that runs it): C — minor reproducibility presentation issue; human did not raise this
- Finding 13 (partrans block omits rho and eta from logit transformation): C — minor; human did not raise this
- Finding 14 (data loaded from remote GitHub URL): C — minor reproducibility dependency; human did not raise this
- Finding 15 (no simulation-based diagnostics comparing filtered vs. forward simulations): C — minor; human did not raise this

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
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
- Human Issue #6: missed
- Human Issue #7: contradiction (Doug says no ESS monitoring was done; human says ESS was observed and often close to zero)
- Human Issue #8: missed
- Human Issue #9: missed

**Findings classification:**
- Finding 1 (accumulator variable accumulates recoveries not cases): A — H += dN_IR is a fundamental specification error; human did not raise this
- Finding 2 (smoothed data fed to binomial measurement model): A — fractional rolling-average inputs to dbinom; human did not raise this specific concern
- Finding 3 (global search initialized from prior mif2 result): A — cooled starting state makes global search ineffective; human did not raise this
- Finding 4 (no quantitative benchmark comparison): A — ARMA and SEIR fitted to different data so log-likelihoods cannot be compared; human did not raise this
- Finding 5 (no profile likelihoods): A — parameter identifiability not assessed; human did not raise this
- Finding 6 (insufficient computational effort; SE too large): A — Np=1000, loglik.se values up to 2355; human did not raise this
- Finding 7 (mu_EI convergence to zero as model misspecification): A — implausible infinite latency not interpreted as misspecification; human did not raise this
- Finding 8 (no model diagnostics including ESS): F — Doug says ESS monitoring is absent; human says ESS was observed and was often close to zero (contradicts Human Issue #7)
- Finding 9 (rho fixed without justification or sensitivity analysis): A — reporting rate fixed at 0.1 with no sensitivity; human did not raise this
- Finding 10 (HP filter lambda inappropriate for daily data): C — lambda=100 designed for quarterly data; human did not raise this
- Finding 11 (ARMA on HP-filtered vs SEIR on smoothed: comparison invalid): C — models on incommensurable observation series; human did not raise this
- Finding 12 (data loaded from GitHub URL, not local file): C — reproducibility concern; human did not raise this
- Finding 13 (partrans omits logit for eta): C — eta can drift outside (0,1) during IF2; human did not raise this
- Finding 14 (no forecast from fitted SEIR model): C — no forward predictions generated; human did not raise this
- Finding 15 (initial conditions fixed, not estimated): C — E(0) and I(0) fixed with no sensitivity analysis; human did not raise this

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 1 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: contradiction (AI says ADF/KPSS tests provide "a principled basis for the detrending decision" (strength S4); human says ADF is not appropriate for this case)
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: covered (matched by finding: "Presentation — reference list non-functional")

**Findings classification:**
- 21.11.1: A — H initialisation error corrupts measurement model (code bug causing filter failures)
- 21.11.2: A — log-likelihood optimum based on single unreplicated pfilter evaluation
- 21.11.4: A — no quantitative benchmark comparison between ARMA and SEIR models
- 21.11.5: A — rho fixed at 0.1 without estimation or profile likelihood
- 21.11.6: A — no profile likelihoods or confidence intervals for any free SEIR parameter
- 21.11.CON: C — population conservation violated at initialisation (compartments sum > N)
- 21.11.7: C — eta not included in logit parameter transformation
- 21.11.8: C — HP filter lambda = 100 inappropriate for daily data
- 21.11.9: C — weekly periodicity in ARMA residuals not addressed
- 21.11.3: C — confusing presentation: ARMA(1,1) output shown in ARMA(2,2) section
- Presentation: D — reference list non-functional (only "here" as link text, no bibliographic metadata) (matches Human Issue #9)
- S4: F — ADF/KPSS tests described as providing "a principled basis for the detrending decision" (contradicts Human Issue #2, which says ADF is not appropriate for this case)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 1 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 6 | 7 | 8 | 5 |
| B (AI major, human also found) | 1 | 1 | 0 | 0 |
| C (AI minor, human missed) | 8 | 7 | 6 | 5 |
| D (AI minor, human also found) | 0 | 0 | 0 | 1 |
| E (Human found, AI missed) | 8 | 7 | 8 | 7 |
| F (Human-AI contradiction) | 0 | 0 | 1 | 1 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 1 | 0 | 8 | 1/9 = 11% | 6 | 8 | 14/15 = 93% |
| Charlie | 1 | 0 | 7 | 2/9 = 22% | 7 | 7 | 14/15 = 93% |
| Doug | 0 | 0 | 8 | 0/8 = 0% | 8 | 6 | 14/14 = 100% |
| Evan | 0 | 1 | 7 | 1/8 = 12% | 5 | 5 | 10/11 = 91% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #1: Section 2: What is the shaded region around the trend line? Is it meaningful in this situation? (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #3: Section 3. If you decide to test for stationarity with ADF or similar, and you conclude there is nonstationarity, then fitting a stationary model is not a natural next step. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #4: Section 4. The POMP model implemented is not an ODE system, so it is best not to write it as one. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #5: From the simulations, you can see that the variability in the data is much higher than the simulations, which follow a smooth curve with little stochasticity. This is the first of many warning signs about what is wrong with the model. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #8: The project mentions the possibility of trying models with additional variability, but does not get around to doing it. For a 5-person group, some subset could have been delegated this task. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 5 out of 9 human issues (56%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #7: Effective sample size is often close to zero, which is another indication of insufficient stochasticity in the model. Modeling multiple COVID waves is not easy: see Projects 13 and 15 for successful approaches. (Covered only by Charlie)
- Human Issue #9: References should follow a standard format. Links are helpful, but one should be able to look through the reference list without clicking on each one. (Covered only by Evan)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 1 |
| Doug | 0 |
| Evan | 1 |
