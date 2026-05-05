# Ned-Clean Analysis — W24 Project 16

---

## Human Issues

1. The introduction has no references and makes exaggerated claims in elaborate language, which may indicate use of ChatGPT.
2. auto.arima is used to identify an ARIMA model without explanation of what it does; alternatively, a simpler analysis that is fully understood would be preferable.
3. ARMA modeling for population dynamics may work better on a log scale.
4. Figures could have numbers and captions to help the reader.
5. Given the weak identifiability, the appropriate conclusions from this study should be fairly inconclusive.
6. Comment on the ARIMA benchmark to assess the fit of the mechanistic model; log-ARMA might be a more competitive challenge.
7. In the formula for S_u, vac_rate should read (1-vac_rate); the text has an error but the code is correct.
8. References are listed at the end but not cited in the text.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "ARIMA section adds limited value, not integrated quantitatively")
- Human Issue #7: covered (matched by finding: "S_u formula uses vaccinationRate instead of (1-vaccinationRate) in text")
- Human Issue #8: missed

**Findings classification:**
- Major #1 (decoupled sub-populations / no cross-infection): A — epidemiologically incoherent model; vaccinated and unvaccinated branches fully isolated
- Major #2 (S_u initialization formula error in text): B — text uses vac_rate for S_u instead of (1-vac_rate) (matches Human Issue #7)
- Major #3 (accumulator H counts recoveries not infections): A — fundamental mismatch between measurement model and data
- Major #4 (rho applied twice / double-discounting H): A — measurement model doubly incorrect
- Major #5 (no simulation from fitted model): A — no visual check that model can reproduce observed data
- Major #6 (profile likelihood plots not genuine profiles): A — scatter plots from global search, not true profiles; CIs invalid
- Major #7 (MIF2 convergence not demonstrated before global search): A — no quantitative evidence of local search convergence
- Major #8 (conceptual error: "negative log likelihood maximum = likelihood minimum"): A — text misidentifies the reported log-likelihood
- Minor #9 (dispersion parameter k fixed without justification): C — no sensitivity analysis or rationale for k=10
- Minor #10 (data subsetting logic fragile): C — hard-coded row indices not validated against ORIGIN_SOURCE column
- Minor #11 (population N = 17.7M but sentinel surveillance data): C — susceptible pool orders of magnitude too large for sentinel observations
- Minor #12 (notation inconsistency: mu_SE in diagram vs Beta in code): C — model diagram misleading relative to code parameterization
- Minor #13 (mu_IR_v < mu_IR_u interpretation speculative): C — conclusion unsupported given model structural flaws
- Minor #14 (ARIMA section adds limited value, not integrated): D — no quantitative ARIMA-POMP comparison (matches Human Issue #6)
- Minor #15 (reproducibility broken: mismatched RDS paths, personal absolute path): C — cluster script and Rmd read different file paths; non-reproducible

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "No non-mechanistic benchmark comparison")
- Human Issue #7: covered (matched by finding: "Initialization formula error: text and code give different S_u formula")
- Human Issue #8: missed

**Findings classification:**
- Major #1 (force-of-infection treats populations as fully isolated): A — no cross-transmission between vaccinated and unvaccinated
- Major #2 (MLE vaccinated recovery rate biologically absurd — 12-year infectious period): A — mu_IR_v = 0.00151/week at MLE; sign of misspecification not flagged by authors
- Major #3 (no non-mechanistic benchmark comparison): B — ARIMA never compared quantitatively against SEIR (matches Human Issue #6)
- Major #4 (pseudo-profile plots non-standard and mislabeled): A — scatter-filter of global search presented as profile likelihood
- Major #5 (global search starting values conflict with bounds; MLE outside search box): A — mu_IR_v MLE two orders of magnitude below stated lower bound
- Major #6 (no quantitative goodness-of-fit or model diagnostics): A — no simulation overlaid on data, no ESS traces, no conditional log-likelihood plot
- Major #7 (initialization formula error: S_u text vs code): B — text states vaccinationRate for S_u; code correctly uses (1-vac_rate) (matches Human Issue #7)
- Major #8 (inconsistent mif2 parameters: Rmd vs run.r): A — materially different optimization settings between scripts with no explanation
- Minor #9 (inconsistency between stated goal and model output): C — vaccine effectiveness inferred indirectly rather than via explicit efficacy parameter
- Minor #10 (profile plots use inconsistent loglik cutoff thresholds without justification): C — some plots filter at -15, others at -10, with no explanation
- Minor #11 (ARIMA section incorrectly concludes SARIMA is inappropriate): C — absence of seasonality in one season is expected and trivial; conclusion misleading
- Minor #12 (hard-coded absolute path in run.r): C — run.r cannot be executed by any other user
- Minor #13 (k overdispersion fixed without justification): C — no sensitivity analysis or rationale for k=10
- Minor #14 (no seed for parallel doParallel local search): C — local search results not reproducible across runs
- Minor #15 (typos and minor presentation issues): C — "Forcast," "immunocompromized," "slighlty," "inmuen systems"; pairs plot axes not discussed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "Severe parameter non-identifiability; conclusions unsupported")
- Human Issue #6: covered (matched by finding: "No non-mechanistic benchmark comparison")
- Human Issue #7: covered (matched by finding: "Single equation for S_u initialization is incorrect in text")
- Human Issue #8: missed

**Findings classification:**
- Major #1 (accumulator tracks recoveries not infections): A — H += dN_IR fits recovery counts against detection data; rho ~ 0.003 implausibly low
- Major #2 (no cross-population transmission — two independent epidemics): A — force of infection uses only same-group I; no mixing between vaccinated and unvaccinated
- Major #3 (profile likelihood plots misidentified global-search scatter plots): A — no profile IF2 run; chi-squared CI cutoff has no statistical justification
- Major #4 (global IF2 search initialized from local search result — anti-pattern): A — inherits terminal cooling schedule; effectively few functional iterations from random starts
- Major #5 (severe parameter non-identifiability; conclusions unsupported): B — within 2 log-lik units, Beta_v ranges 0.30–23.6; best-fit row shows Beta_v > Beta_u, opposite of paper's claim (matches Human Issue #5)
- Major #6 (no non-mechanistic benchmark comparison): B — ARIMA AIC reported but POMP AIC not; no formal comparison (matches Human Issue #6)
- Major #7 (k dispersion parameter fixed without justification): A — fixed at 10 with no rationale or sensitivity analysis
- Major #8 (misleading statement about log-likelihood): A — paper calls -193.66 a "likelihood minimum" but this is logmeanexp of log-likelihoods
- Minor (no simulation vs data plot): C — run.r generates simulation plot but it does not appear in rendered output
- Minor (convergence traces inadequately presented): C — Rmd traces use Nmif=300 but global search uses Nmif=1000; inconsistency unexplained
- Minor (hard-coded absolute path in run.r): C — author-specific absolute path prevents reproduction
- Minor (typos and grammatical errors): C — "Forcast," "computationally intesive," "inmuen," "slighlty"
- Minor (S_u initialization incorrect in text): D — text states vaccinationRate; code correctly uses (1-vac_rate) (matches Human Issue #7)
- Minor (no model diagnostics): C — no conditional log-likelihood per time point, no ESS plot, no filtering distribution
- Minor (initial condition I_v and I_u hardcoded to 1): C — sensitivity to this assumption not discussed
- Minor (no quantitative goodness-of-fit summary): C — log-likelihood quoted without context; no AIC, no model comparison table

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "Profile likelihood plots not proper profiles; key parameters unidentified — central scientific claim cannot be supported")
- Human Issue #6: covered (matched by finding: "No quantitative benchmark comparison of ARIMA vs POMP")
- Human Issue #7: covered (matched by finding: "Initial condition formula for S_u appears erroneous")
- Human Issue #8: missed

**Findings classification:**
- Major 24.16.2/3 (profile likelihood plots not proper profiles; key parameters unidentified): B — scatter plots from global search; near-MLE Beta_v scattered across 0–20; claim Beta_v < Beta_u unsupported (matches Human Issue #5)
- Major 24.16.4 (measurement model not stated in paper): A — rho and k appear in code with no mathematical definition in text
- Major 24.16.1 (initial condition formula for S_u erroneous): B — text states vaccinationRate for S_u; should be (1-vaccinationRate) (matches Human Issue #7)
- Major 24.16.5 (mif2 convergence trace plots absent): A — no trace plots of log-likelihood or parameters over IF2 iterations
- Major 24.16.6 (no quantitative benchmark comparison of ARIMA vs POMP): B — ARIMA loglik = -211.2 and POMP loglik = -193.7 are directly comparable but never compared (matches Human Issue #6)
- Major 24.16.7 (causal language used without causal identification): A — "proves that vaccinations effectively slows down the transmission rate" is a causal claim from observational analysis
- Minor 24.16.13 (negative spike in conditional log-likelihood not discussed): C — severe conditional log-lik drop at epidemic peak onset not commented on
- Minor misc (multiple notation and presentation issues): C — mu_SE_v in diagram vs Beta_v in code; typos "Forcast," "intesive," "inmuen"
- Minor misc-2 (pairs plot very low resolution and nearly illegible): C — parameter space coverage cannot be assessed from rendered plot

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 3 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 7 | 6 | 6 | 3 |
| B (AI major, human also found) | 1 | 2 | 2 | 3 |
| C (AI minor, human missed) | 6 | 7 | 7 | 3 |
| D (AI minor, human also found) | 1 | 0 | 1 | 0 |
| E (Human found, AI missed) | 6 | 6 | 5 | 5 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

**Alex**
- Human Recall = (B+D) / (B+D+E) = (1+1) / (1+1+6) = 2/8 = 0.250
- AI-Unique Rate = (A+C) / (A+B+C+D) = (7+6) / (7+1+6+1) = 13/15 = 0.867

**Charlie**
- Human Recall = (B+D) / (B+D+E) = (2+0) / (2+0+6) = 2/8 = 0.250
- AI-Unique Rate = (A+C) / (A+B+C+D) = (6+7) / (6+2+7+0) = 13/15 = 0.867

**Doug**
- Human Recall = (B+D) / (B+D+E) = (2+1) / (2+1+5) = 3/8 = 0.375
- AI-Unique Rate = (A+C) / (A+B+C+D) = (6+7) / (6+2+7+1) = 13/16 = 0.813

**Evan**
- Human Recall = (B+D) / (B+D+E) = (3+0) / (3+0+5) = 3/8 = 0.375
- AI-Unique Rate = (A+C) / (A+B+C+D) = (3+3) / (3+3+3+0) = 6/9 = 0.667

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover (5 out of 8):

1. **Human Issue #1** — Introduction has no references; exaggerated claims; possible ChatGPT use. Missed by all four reviewers.
2. **Human Issue #2** — auto.arima used without explanation; simpler or better-explained alternative preferable. Missed by all four reviewers.
3. **Human Issue #3** — ARMA modeling for population dynamics may work better on a log scale. Missed by all four reviewers.
4. **Human Issue #4** — Figures could have numbers and captions. Missed by all four reviewers.
5. **Human Issue #8** — References are listed at the end but not cited in the text. Missed by all four reviewers.

**Count: 5 out of 8 human issues were missed by every reviewer.**

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #5 (weak identifiability → inconclusive conclusions): covered by Doug and Evan; not unique to either.
- Human Issue #6 (ARIMA benchmark comment): covered by all four reviewers; not unique to any.
- Human Issue #7 (S_u formula error): covered by all four reviewers; not unique to any.

No reviewer has a unique find — every human issue that was covered was covered by at least two reviewers.

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |

### Universal AI-only flags

Issues raised as a concern by every reviewer that the human did not mention:

1. **Profile likelihood plots are not genuine profile likelihoods** — all four reviewers (Alex Major #6, Charlie Major #4, Doug Major #3, Evan Major 24.16.2/3) independently flagged that the "profile likelihood" plots presented are scatter plots from the global search, not true profiles computed by fixing the focal parameter and optimizing over all others. The chi-squared confidence interval cutoffs applied to these plots are therefore statistically invalid. The human reviewer did not raise this concern.

**Count: 1 universal AI-only flag.**
