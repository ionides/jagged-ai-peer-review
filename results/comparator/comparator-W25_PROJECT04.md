# Comparator Analysis — W25 Project 04

---

## Human Issues

1. The introduction is brief and does not outline goals of the project or relevant background information.

2. The interpretation of ARMA residuals is poor, "The residual time series appears centered around zero with no clear patterns." The time plot of residuals shows extreme heteroskedasticity. The residual diagnostics are trying to remind the team that they should consider a logarithmic transformation. Also, the residuals are long-tailed compared to normal.

3. The roots on, and close to, the unit circle suggest poor stability. Thus, the conclusion that "the roots confirm stationarity and invertibility" is weak. There's no point looking at diagnostic plots if you ignore what they are telling you.

4. The ARMA benchmark should be carried out as log-ARMA for situations where ARMA fits better on a log scale, as in Chapter 18 (measles case study).

5. It is hard to interpret the value of a log-likelihood as an argument for or against the model; usually, log-likelihood is useful only to compare models. Thus, there is weak reasoning in the conclusion: "Given the relatively large sample size and the complexity of the data (confirmed, recovered, and deceased cases), this log-likelihood value suggests that the VAR(9) model provides a reasonable fit to the data, capturing the main dynamics without overfitting."

6. The Fig 5 residual plot is showing the log-scale variation that is reminded to use a logarithmic transformation of the data. The explanation of this figure as "no clear patterns, although some variance increases during peaks" makes two incompatible points; first saying there is not a pattern and then identifying one.

7. The report references a previous project that was influential for their analysis. The report could do a better job explaining explicitly what they learned from that project and what their own creative innovations were. This project made plenty of its own contributions, but the reader should not have to go to past projects to assess this.

8. Innovative use of a vector autoregressive (VAR) model. However, it is not clear how this supports substantial conclusions.

9. Erratic use of boldface makes the text harder to read.

10. Incorrect reasoning: "The ACF and PACF plots for confirmed, recovered, and deceased cases show strong autocorrelation and slow decay, indicating non-stationarity and the need for differencing". The usual motivation for the sample ACF assumes a stationary model. Also, differencing is only one way to build a non-stationary model.

11. Fig 1 needs a different scale for deceased. That line is not legible in its current form.

12. ARIMA(5,1,5) is a large model, but also it is not the model with lowest AIC. How about ARIMA(1,1,3) or (1,1,4)?

13. VAR is described as "more transparent" and "easier to interpret". Yet, no useful interpretation of this model is provided.

14. VAR diagnostics show longer than normal tails. A time plot (not shown) would also reveal heteroskedasticity.

15. "The fitted values closely capture the major trends and variations in the data, supporting the use of the VAR model for analyzing the dynamic relationships between these pandemic variables." Authors should check whether using last week to predict this week is detectably worse.

16. Fig 4 has a typo in the time axis (it runs 2024 - 2041).

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
- Human Issue #9: missed
- Human Issue #10: missed
- Human Issue #11: missed
- Human Issue #12: covered (matched by finding: "ARIMA(5,1,5) not checked for near-cancellation of AR and MA roots, indicating possible over-parameterization")
- Human Issue #13: missed
- Human Issue #14: missed
- Human Issue #15: missed
- Human Issue #16: missed

**Findings classification:**
- Finding 1 (R compartment missing dN_RS outflow): A — critical bug: R compartment never depleted, population not conserved across all SEIRS variants
- Finding 2 (H accumulates recoveries instead of new infections): A — observation model mis-specified; H should count new infections, not I→R transitions
- Finding 3 (typographical error in piecewise parameter definition): A — text states third period as [63, 119], creating overlap with second period; code is correct but description is misleading
- Finding 4 (profile likelihood for Eta omits mu_IR from random walk): A — mu_IR frozen during Eta profile, producing unreliable CIs
- Finding 5 (AIC comparison between ARIMA and SEIRS invalid): A — log-likelihoods are on incompatible scales across model classes; comparison is methodologically invalid
- Finding 6 (time series objects created with frequency=7): A — weekly data should use frequency=52 or 1; incorrect frequency affects time axis labeling and ACF/PACF lag scale interpretation
- Finding 7 (VAR lag selection discards IC recommendations without justification): C — p=9 chosen over IC-optimal ~20 without formal justification
- Finding 8 (VAR log-likelihood computed via incorrect manual formula): C — manual formula may not equal true ML log-likelihood; vars package logLik method not used
- Finding 9 (mu_RS fixed at 0.005 without epidemiological basis): C — 200-week immunity period unjustified; circular reasoning used to defend the fixed value
- Finding 10 (profile CI thresholds use inconsistent filtering): C — threshold computed on unfiltered data but CI extracted from filtered subset, admitting high-SE points
- Finding 11 (initial state I=1000 not justified): C — hardcoded initial infectious count with no sensitivity analysis or estimation
- Finding 12 (ARIMA(5,1,5) not checked for near-cancellation of AR/MA roots): D — near-unit-circle MA roots noted but no near-cancellation diagnostic run; model may be over-parameterized (matches Human Issue #12)
- Finding 13 (figure references internally inconsistent): C — chunk label numbering offset from text references for at least Figures 4–6
- Finding 14 (global search 2 does not use a fresh Latin hypercube design): C — second global search effectively a local search from a previous profile point
- Finding 15 (NegBinom parameterization uses non-standard mean-variance form without clarification): C — unusual parameterization style unexplained relative to R's dnbinom_mu implementation

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 15 |
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
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed
- Human Issue #11: missed
- Human Issue #12: missed
- Human Issue #13: missed
- Human Issue #14: missed
- Human Issue #15: missed
- Human Issue #16: missed

**Findings classification:**
- Major 1 (R compartment bug): A — R compartment never decremented by dN_RS, violating population conservation across all SEIRS models
- Major 2 (near-zero b3): A — b3 ≈ 0.0024 during largest wave accepted without misspecification investigation
- Major 3 (Model 2 unconverged): A — SEIRS Model 2 log-likelihood still rising at 200 iterations; results unreliable
- Major 4 (mu_RS fixed): A — mu_RS fixed at 0.005 without profile likelihood or sensitivity analysis
- Major 5 (no post-fit ESS): A — ESS shown only for initial guess, not after local or global search
- Minor (piecewise boundary typo): C — third interval written as [63,119] in text but code implements [97,119]
- Minor (I₀ = 1000 unjustified): C — initial infectious count of 1000 inconsistent with documented 3 cases in Kerala
- Minor (figure caption/reference mismatch): C — text calls ARIMA fitted-values plot "Figure 5" but chunk is labeled fig4
- Minor (hard-coded local path): C — commented-out absolute path "/Users/cathy/Desktop/..." in code
- Minor (vaccine data not modeled): C — vaccination data present but no vaccinated compartment in SEIRS
- Minor (rho3 unexplained): C — Model 2 rho3 ≈ 0.09 described as unexplainable rather than flagged as misspecification signal
- Minor (no formal SEIRS variant comparison): C — four SEIRS variants developed with no LRT or AIC comparison table
- Minor (rho2 profile uninvestigated): C — messy rho2 profile attributed to computation and dismissed without further investigation
- Minor (AIC parameter count inconsistency): C — code sets seirs_best_model_num=12 but ARIMA(5,1,5) has 11 free parameters; unexplained
- Minor (no SEIRS vs. SEIR comparison): C — paper motivates SEIRS over SEIR biologically but never formally tests this with a fitted SEIR model

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 10 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 16 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "ARIMA(5,1,5) near non-invertibility — several MA roots near/on unit circle, same underlying concern about roots suggesting poor model conditioning")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed
- Human Issue #11: missed
- Human Issue #12: covered (matched by finding: "ARIMA(5,1,5) near non-invertibility — questions why ARIMA(5,1,5) is preferred despite parsimony concerns, same underlying issue as human's 'not the lowest AIC' point")
- Human Issue #13: missed
- Human Issue #14: missed
- Human Issue #15: missed
- Human Issue #16: missed

**Findings classification:**
- Finding 1 (Pseudo-profiles): A — all profile likelihoods are pseudo-profiles; profiled parameter never fixed during optimization
- Finding 2 (Profile guess stratification): A — profile guess stratification groups by mu_IR regardless of which parameter is being profiled
- Finding 3 (Global search initialization): A — global search inherits cooling schedule from local search chain, undermining genuine global exploration
- Finding 4 (Accumulator variable H): A — H accumulates recoveries (dN_IR) rather than new infections, mismatching the observation data
- Finding 5 (Invalid LL/AIC comparison): A — log-likelihood and AIC comparison between ARIMA and SEIRS models is invalid due to different observation model distributions
- Finding 6 (mu_RS implausible): A — mu_RS fixed at biologically implausible value (200-week immunity) with no sensitivity analysis
- Finding 7 (No valid benchmark): A — no non-mechanistic statistical benchmark with matching observation model for the SEIRS model
- Finding 8 (Piecewise interval typo): C — third piecewise interval stated as [63, 119] but should be [97, 119]; documentation-only error
- Finding 9 (Time series frequency): C — ts objects created with frequency=7 instead of frequency=52, causing incorrect spectral/ACF lag labeling
- Finding 10 (Rho2 profile drops best row): C — highest log-likelihood row silently dropped without justification in rho2, eta profiles, and seirs_global2
- Finding 11 (Initial I(0)=1000): C — initial infected count fixed at 1000 without justification or sensitivity analysis
- Finding 12 (VAR LL approximation): C — VAR log-likelihood manually computed using approximation rather than directly from the model
- Finding 13 (ARIMA parsimony/invertibility): D — ARIMA(5,1,5) near non-invertibility with MA roots near unit circle; model selection ignores parsimony (matches Human Issues #3 and #12)
- Finding 14 (Figure cross-referencing errors): C — figure caption text not synchronized with chunk labels; numbering inconsistencies throughout
- Finding 15 (ChatGPT disclosure): C — AI use disclosure lacks specificity about which analyses or code sections used AI assistance

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 14 |
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
- Human Issue #10: missed
- Human Issue #11: missed
- Human Issue #12: missed
- Human Issue #13: missed
- Human Issue #14: missed
- Human Issue #15: missed
- Human Issue #16: missed

**Findings classification:**
- C1: A — log-likelihood comparison between ARIMA and SEIRS is on different scales (different data transformations), making the central quantitative improvement claim invalid
- C2: A — phase boundary overlap (weeks 63–96 assigned to both Phase 2 and Phase 3) makes the model specification mathematically ill-defined
- C3: A — global search convergence diagnostics absent for both SEIRS models; no scatter plots or log-likelihood distribution across runs
- C4: A — ESS not shown for final fitted parameter estimates, leaving reliability of reported log-likelihood values uncertain
- C5: A — final log-likelihood values not confirmed as replicated pfilter estimates; unclear whether they come from mif2 internal (biased) or replicated pfilter
- C6: A — mu_RS fixed at biologically implausible value without profile likelihood or sensitivity analysis
- C7: A — near-zero b3 in Model 1 contradicts mechanistic attribution of the third wave to Omicron transmissibility
- C8: C — profile likelihoods missing for b3, rho_3 (Model 2), and mu_EI despite acknowledged identifiability concerns
- C9: C — NegBinom parameterization convention not stated, hindering reproducibility
- C10: C — initial compartment allocations for E0, I0, R0 not stated; only S0 = eta*N is specified
- MS3: C — global search range for b3 stated as [10, 50] but best result is b3 ≈ 0.0024, far below the stated floor

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 16 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 6 | 5 | 7 | 7 |
| B (AI major, human also found) | 0 | 0 | 0 | 0 |
| C (AI minor, human missed) | 8 | 10 | 7 | 4 |
| D (AI minor, human also found) | 1 | 0 | 1 | 0 |
| E (Human found, AI missed) | 15 | 16 | 14 | 16 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 0 | 1 | 15 | 1/16 = 6% | 6 | 8 | 14/15 = 93% |
| Charlie | 0 | 0 | 16 | 0/16 = 0% | 5 | 10 | 15/15 = 100% |
| Doug | 0 | 1 | 14 | 2/16 = 12% | 7 | 7 | 14/15 = 93% |
| Evan | 0 | 0 | 16 | 0/16 = 0% | 7 | 4 | 11/11 = 100% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #1: The introduction is brief and does not outline goals of the project or relevant background information. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #2: The interpretation of ARMA residuals is poor, "The residual time series appears centered around zero with no clear patterns." The time plot of residuals shows extreme heteroskedasticity. The residual diagnostics are trying to remind the team that they should consider a logarithmic transformation. Also, the residuals are long-tailed compared to normal. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #4: The ARMA benchmark should be carried out as log-ARMA for situations where ARMA fits better on a log scale, as in Chapter 18 (measles case study). (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #5: It is hard to interpret the value of a log-likelihood as an argument for or against the model; usually, log-likelihood is useful only to compare models. Thus, there is weak reasoning in the conclusion: "Given the relatively large sample size and the complexity of the data (confirmed, recovered, and deceased cases), this log-likelihood value suggests that the VAR(9) model provides a reasonable fit to the data, capturing the main dynamics without overfitting." (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #6: The Fig 5 residual plot is showing the log-scale variation that is reminded to use a logarithmic transformation of the data. The explanation of this figure as "no clear patterns, although some variance increases during peaks" makes two incompatible points; first saying there is not a pattern and then identifying one. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #7: The report references a previous project that was influential for their analysis. The report could do a better job explaining explicitly what they learned from that project and what their own creative innovations were. This project made plenty of its own contributions, but the reader should not have to go to past projects to assess this. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #8: Innovative use of a vector autoregressive (VAR) model. However, it is not clear how this supports substantial conclusions. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #9: Erratic use of boldface makes the text harder to read. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #10: Incorrect reasoning: "The ACF and PACF plots for confirmed, recovered, and deceased cases show strong autocorrelation and slow decay, indicating non-stationarity and the need for differencing". The usual motivation for the sample ACF assumes a stationary model. Also, differencing is only one way to build a non-stationary model. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #11: Fig 1 needs a different scale for deceased. That line is not legible in its current form. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #13: VAR is described as "more transparent" and "easier to interpret". Yet, no useful interpretation of this model is provided. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #14: VAR diagnostics show longer than normal tails. A time plot (not shown) would also reveal heteroskedasticity. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #15: "The fitted values closely capture the major trends and variations in the data, supporting the use of the VAR model for analyzing the dynamic relationships between these pandemic variables." Authors should check whether using last week to predict this week is detectably worse. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #16: Fig 4 has a typo in the time axis (it runs 2024 - 2041). (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 14 out of 16 human issues (88%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #3: The roots on, and close to, the unit circle suggest poor stability. Thus, the conclusion that "the roots confirm stationarity and invertibility" is weak. There's no point looking at diagnostic plots if you ignore what they are telling you. (Covered only by Doug)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 1 |
| Evan | 0 |
