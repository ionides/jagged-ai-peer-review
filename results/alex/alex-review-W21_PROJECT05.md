# Peer Review: W21 Project 05 — Seasonal Influenza in Michigan (POMP Models)

---

## Summary

This project investigates seasonal influenza A in Michigan using the CDC FluView dataset, focusing on the 2019–20 season. Three POMP models are implemented: a standard SIR, an SEIR, and a modified SIR with a hard-coded contact-rate reduction after week 22. The analysis stops at local search; no global search, profile likelihoods, or confidence intervals are produced. The project is incomplete relative to standard POMP analysis expectations, and several methodological and coding errors further undermine its conclusions.

---

## Weaknesses (Most Critical First)

### 1. [Major] No Global Search — Analysis Terminates Prematurely

The entire parameter optimization consists of a single local search starting from one set of hand-chosen initial values. No global search (e.g., multi-start `mif2` from a Latin hypercube or random box) is attempted for any model. The conclusion that "all three models are not appropriate" is therefore unsupported: poor local-search behavior near one starting point does not establish that no good parameter region exists. Profile likelihoods and confidence intervals are explicitly omitted. This is the most critical omission, as it makes the inferential conclusions unreliable.

### 2. [Major] Code Bug: SIR2 Likelihood Block Prints the Wrong Result

In the chunk `SIR2_init_lik`, the code computes `sir2_L_pf` for the third model but then prints `sir_L_pf` (the first model's likelihood):

```r
print(sir_L_pf)   # should be print(sir2_L_pf)
```

This means the reported initial-guess likelihood for the third model is actually the first model's likelihood. The reader cannot determine the true initial likelihood of the time-varying SIR model from the writeup.

### 3. [Major] Hard-Coded Contact-Rate Reduction Is Not a Learned Parameter

The third model multiplies Beta by a fixed constant (0.7) after week 22. This multiplier is never estimated — it is not included in `paramnames`, not perturbed by `rw.sd`, and not optimized by `mif2`. The model therefore does not actually learn the magnitude of the contact-rate change from data; the 30% reduction is an arbitrary assumption. The stated research question — "Is it possible to model the **change** of contact rate?" — is not answered by fixing the change a priori.

### 4. [Major] Measurement Model Inappropriate: H Accumulates Without Reset Between Observations

In the SIR step, `H += dN_IR` accumulates recovered individuals since the last reset (via `accumvars="H"`). The `dmeas` and `rmeas` snippets then model `reports ~ Binomial(H, rho)`. However, H counts the cumulative number of recoveries within each observation interval, not the number of new infections detected. Influenza reports from clinical labs represent new positive tests, not cumulative recoveries. This conflation of incidence accumulation with reported cases is a serious mismatch between what the data represent and what the model generates.

### 5. [Major] No Overdispersion in Measurement Model Despite Clear Evidence of Need

The conclusion explicitly acknowledges that "over-dispersed model such as negative binomial is suggested," yet all three models use strictly binomial measurement. Given the visible double-peak structure in the data and the NaN/divergent likelihoods encountered, the failure to even attempt a negative binomial model (or add a noise parameter) is a significant analytical gap.

### 6. [Major] NaN Log-Likelihoods Accepted Without Diagnosis

The text notes that models 1 and 3 suffer from "NaN log-likelihood" during local search and accepts this as evidence of model failure, with no attempt to diagnose the cause. Common causes — particle filter degeneracy, parameter values outside feasible bounds, or numerical overflow in the Csnippet — are not investigated. The resolution to simply abandon these models is not scientifically justified.

### 7. [Major] Only One Flu Season Modeled Despite Multi-Season Data

The exploratory analysis covers five flu seasons (2016–21) and motivates the study by comparing season patterns. Yet only a single season (2019–20) is fitted. The COVID-19 contact-rate hypothesis could have been tested more rigorously by fitting shared parameters across seasons with a season-specific contact-rate modifier, or at least by fitting multiple seasons separately for comparison.

### 8. [Minor] Highly Unstable Local Search: Only 50 Iterations, Np = 2000

The `mif2` runs use `Nmif=50` and `Np=2000`. For influenza data with a population of ~10 million, 2,000 particles is very small and 50 iterations is typically insufficient for convergence. The trace plots described as "bouncing around" are consistent with inadequate particle counts rather than fundamental model failure. Increasing `Np` to at least 5,000–10,000 and `Nmif` to 100–200 is standard practice.

### 9. [Minor] Likelihood Comparison Across Models Is Informal and Incomplete

Model comparison is performed informally by visual inspection of simulations and narrative comparison of loglikelihood point estimates. No formal criterion (AIC, likelihood ratio test) is applied. The best log-likelihoods achieved are -940 (SIR), -861 (SEIR), and -333 (SIR2), but these are not compared in a table, and the SIR2 result contradicts the textual conclusion that "the second model seems to be a better fit."

### 10. [Minor] Conclusion Contradicts the Likelihood Evidence

The best log-likelihood from the local search is -333 for the third model (SIR with time-varying contact rate), substantially better than -861 for SEIR. Yet the conclusion states "the second model seems to be a better fit." This is internally inconsistent with the saved CSV data and undermines trust in the analysis.

### 11. [Minor] `reports` Variable Represents Raw Counts but Percent Positive Is the More Reliable Observable

The modeling dataset uses raw positive test counts (`TOTAL.A`) rather than percent positive or test-adjusted counts. Because the total number of specimens tested (`TOTAL.SPECIMENS`) varies week to week, raw counts conflate true incidence with testing intensity. Using percent positive or modeling the number of positives out of total tests (binomial with varying denominator) would be more appropriate.

### 12. [Minor] No Sensitivity Analysis or Uncertainty Quantification for Fixed Parameters

`N` (Michigan population, 9.984e6) and the COVID contact-rate multiplier (0.7) are fixed without sensitivity checks. Since `eta` determines the initial susceptible fraction, fixing N while estimating eta implies strong prior knowledge of susceptibility; this assumption is never discussed.

### 13. [Minor] SEIR Model: Latency Rate `mu_EI` Converges to Implausibly Large Values

The best SEIR parameters show `mu_EI = 16.67` per week, implying a mean latent period of less than one day (1/16.67 weeks ≈ 0.4 days). The known influenza latent period is 1–4 days. These biologically implausible values are reported without comment, suggesting the SEIR model is not identifiable from these data or is misspecified, but this is not analyzed.

### 14. [Minor] Figure Captions Reference Incorrect Date Ranges

Figure 1 caption states "2016-17 Season - 2020-21 Season" and mentions "ending April 3rd (13th week), 2021," but the POMP modeling focuses on the 2019-20 season only. The disconnect between exploratory and modeling scopes is confusing and not clearly signposted.

### 15. [Minor] References Section Is Minimal

Only two references are provided: the CDC data source and the course lecture notes. No epidemiological literature on influenza modeling, no citations for the SIR/SEIR frameworks, and no references for the specific `pomp` methodology are included. A project of this scope requires substantially more scholarly grounding.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project05/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project05/sir_lik.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project05/seir_lik.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project05/sir2_lik.csv`
