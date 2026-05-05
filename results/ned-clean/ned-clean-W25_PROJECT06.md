# Ned-Clean Analysis — W25 Project 06

---

## Human Issues

1. Too little time spent on the mechanistic POMP model; difficulties with the POMP model need thoughtful diagnostics to figure out how science and time series data work coherently.
2. MAPE is not comparable between data transformations (unlike log-likelihood which can be adjusted via Jacobian); using elaborate modern methods (VMD, N-BEATS) at the expense of careful use of appropriate methods studied in class.
3. Likelihood is a more efficient inference metric than MAPE; MAPE should also have been calculated for the SEIR model for fair comparison.
4. ADF test is inappropriate and a poor choice given the clear nonstationarity (diminishing peaks); especially inappropriate before taking logs.
5. ARMA residual diagnostics incorrectly claim "no visible trend or seasonal structure" but the residuals show extreme heteroskedasticity; team should consider a logarithmic transformation.
6. The SEIR model should be compared to the ARMA benchmark; fitted SEIR model falls short by 157 log units, suggesting the SEIR model is missing something important.
7. Particle depletion and degeneracy issues are typical of poor model fit; inflexible seasonality modeling or lack of overdispersion may be the issue; diagnostic checks needed.
8. Mean/median summary statistics are not meaningful for time series with dynamic variation; should avoid such statements.
9. For comparing ARMA with log-ARMA, a Jacobian calculation can put log-likelihood and AIC values on the same scale.
10. ACF, PACF, and Box-Ljung for ARMA residuals are almost always uninformative after AIC selection; better to look at normality of residuals (which would show long tails, a clue for log transform).
11. The Outlook section appears to be produced by GenAI; modern methods listed without references or details.

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

**Findings classification:**
- Alex-1 (NewEI accumulation error — wrong compartment tracked, factor-of-7 undercount): A — POMP measurement model critical bug; human did not raise
- Alex-2 (emeas uses cumulative H, inconsistent with dmeas/rmeas): A — measurement model internal inconsistency; human did not raise
- Alex-3 (Model is SEIRS but described as SEIR throughout): A — model labeling error; human did not raise
- Alex-4 (Population N = 2267000 incorrect at 23% of actual population): A — biased force-of-infection; human did not raise
- Alex-5 (amp unconstrained in local mif2 partrans override; amp > 1 causes periodic transmission shutdown): A — partrans override bug; human did not raise
- Alex-6 (Written model equations include birth/death mu and importation lambda absent from code): A — model description vs implementation mismatch; human did not raise
- Alex-7 (Profile likelihood for rho is scatter plot, not profile; CI threshold wrong): A — pseudo-profile and invalid CI; human did not raise
- Alex-8 (Cross-model comparison not equivalent: DL uses 20-county data, ARMA/POMP use national aggregates): A — information asymmetry in comparison; human did not raise
- Alex-9 (VMD decomposition uses full dataset including validation period — data leakage): A — feature-level data leakage; human did not raise
- Alex-10 (ARMA ignores 52-week seasonality; near-unit-circle AR root): C — missing SARIMA; human did not raise
- Alex-11 (ARMA forecast accuracy evaluated in-sample only; inconsistent with DL validation MAPE): C — in-sample vs out-of-sample comparison inconsistency; human did not raise
- Alex-12 (loglik.se filter threshold of 10 too permissive): C — filter too loose; human did not raise
- Alex-13 (start_params undefined in local search code): C — reproducibility issue; human did not raise
- Alex-14 (Duplicate library(pomp) call): C — cosmetic redundancy; human did not raise
- Alex-15 (Beta range 83–748 implausibly wide and unexplained): C — implausible parameter range not discussed; human did not raise

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 9 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 11 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: Charlie-7 "no quantitative ARMA vs POMP comparison on common scale")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: covered (matched by finding: Charlie-12 "AIC comparison between log-ARMA and ARMA invalid without Jacobian correction")
- Human Issue #10: missed
- Human Issue #11: missed

**Findings classification:**
- Charlie-1 (partrans override removes logit constraints on amp and omega; all amp values exceed 2.0): B — wait, this is major and does NOT match any human issue. A — partrans override bug; human did not raise this
- Charlie-2 (Global search initialized from corrupted local mif2 result; inherited broken partrans and anchored cooling): A — global search anti-pattern; human did not raise
- Charlie-3 (Profile likelihood for rho is pseudo-profile; CI threshold wrong at maxloglik - 4): A — invalid profile and CI; human did not raise
- Charlie-4 (Mathematical model in text does not match Csnippet; SEIRS vs SEIR; mu and lambda absent from code): A — model description vs implementation mismatch; human did not raise
- Charlie-5 (Best-fit Beta = 100.4 biologically implausible, R0 ~217; no corroboration with literature): A — biologically implausible parameter; human did not raise
- Charlie-6 (emeas inconsistency with dmeas/rmeas; H not in accumvars, grows without bound): A — measurement model inconsistency; human did not raise
- Charlie-7 (No quantitative ARMA vs POMP comparison on common scale; different observation models): B — matches Human Issue #6
- Charlie-8 (start_params undefined in local search code): A — reproducibility failure; human did not raise
- Charlie-9 (omega not perturbed in rw.sd in either search; never optimized): C — omega not explored; human did not raise
- Charlie-10 (Ljung-Box df not corrected for estimated ARMA parameters; test anti-conservative): C — incorrect test df; human did not raise
- Charlie-11 (Deep learning validation uses only 2-step ahead; train/validation split not described): C — evaluation methodology gaps; human did not raise
- Charlie-12 (AIC comparison between log-ARMA and linear ARMA noted invalid but computed without Jacobian): D — matches Human Issue #9
- Charlie-13 (library(pomp) called twice in setup chunk): C — cosmetic redundancy; human did not raise
- Charlie-14 (melt() from reshape2 used without explicit import): C — dependency issue; human did not raise
- Charlie-15 (No sessionInfo() or package version documentation): C — reproducibility gap; human did not raise

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 9 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: Doug-6 "no benchmark comparison of POMP against ARMA on common basis")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: covered (matched by finding: Doug-17 "log-ARMA and ARMA log-likelihoods described as not comparable but compared by implication")
- Human Issue #10: missed
- Human Issue #11: missed

**Findings classification:**
- Doug-1 (Missing accumvars causes measurement model to use only last Euler sub-step; H grows without bound): A — critical accumvars bug; human did not raise
- Doug-2 (Population N ~22% of actual Hungary population; Beta ~100 is ~20x too high): A — biased force-of-infection; human did not raise
- Doug-3 (Global search initialized from previous mif2 result; cooling schedule already decayed): A — global search anti-pattern; human did not raise
- Doug-4 (amp estimated without transformation constraint; all values exceed 1; transmission shutdowns): A — partrans override bug; human did not raise
- Doug-5 (Profile likelihood is pseudo-profile; CI threshold maxloglik - 4 instead of -1.92; only 3 points in relaxed cutoff): A — invalid profile and CI; human did not raise
- Doug-6 (No benchmark comparison of POMP against ARMA on common basis; different observation models): B — matches Human Issue #6
- Doug-7 (ODE equations claim demographic turnover but Csnippet implements none; reproducibility failure): A — model description vs code discrepancy; human did not raise
- Doug-8 (SEIR vs SEIRS mislabeling — waning immunity present): C — model labeling error; human did not raise
- Doug-9 (CI threshold maxloglik - 4 vs -1.92 detail): C — this is elaboration of Doug-5 already classified as A; treating as additional minor elaboration on a separately listed point. C — CI threshold wrong; human did not raise (note: this is the same concern as Doug-5 but listed as a separate minor bullet)
- Doug-10 (amp upper bound in global search not enforced due to missing constraint): C — constraint not enforced; human did not raise
- Doug-11 (mu_IR lower bound implies implausible infectious period; mu_EI implies 7.4-week latent period): C — biologically implausible parameter bounds; human did not raise
- Doug-12 (H accumulates recoveries not cases; emeas gives nonsensical cumulative total): C — measurement model inconsistency (minor restatement of Doug-1 aspect); human did not raise
- Doug-13 (Deep learning evaluation methodology incompletely described; MAPE comparison with in-sample ARMA invalid): C — evaluation methodology gaps; human did not raise
- Doug-14 (Duplicate library(pomp) call): C — cosmetic redundancy; human did not raise
- Doug-15 (Auto-installing packages in non-interactive Rmd): C — coding best practice violation; human did not raise
- Doug-16 (plan(multicore) unsupported on Windows): C — portability issue; human did not raise
- Doug-17 (Log-ARMA and ARMA log-likelihoods described as not directly comparable but compared by implication): D — matches Human Issue #9
- Doug-18 (Population size N not justified or sourced): C — missing justification for N; human did not raise

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 9 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: Evan-M1 "best POMP log-likelihood not reported; comparing ARMA vs POMP loglik would quantify mechanistic value")
- Human Issue #7: covered (matched by finding: Evan-NEW-B "ESS monitoring absent; standard diagnostic for particle degeneracy")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed
- Human Issue #11: missed

**Findings classification:**
- Evan-M2 (Profile likelihood for rho not valid; CI threshold maxloglik - 4 instead of -1.92): A — invalid profile and CI; human did not raise
- Evan-M5 (amp does not converge in local search; text incorrectly claims "parameters stabilized relatively quickly"): A — non-convergence of key parameter not acknowledged; human did not raise
- Evan-NEW-A (Fitted mu_EI ~0.13-0.16/week implies 7-8 week latent period; varicella incubation is 10-21 days; not acknowledged): A — biologically implausible fitted parameter; human did not raise
- Evan-M9 (Lambda importation term in math description absent from implemented code): A — model description vs implementation discrepancy; human did not raise
- Evan-M4 (No seasonal ARMA component despite strong 52-week periodicity; near-unit-root AR polynomial): C — missing SARIMA; human did not raise
- Evan-M3 (ARMA residual ACF x-axis in normalized units, not lags in weeks): C — display error in diagnostic plot; human did not raise
- Evan-M7 (No common evaluation framework across three methods; DL uses 20-county data vs ARMA/POMP national aggregates): C — information asymmetry in comparison; human did not raise
- Evan-M1 (Best POMP log-likelihood not reported in text; comparing to ARMA loglik would quantify mechanistic value): D — matches Human Issue #6
- Evan-NEW-B (ESS monitoring absent; standard diagnostic for particle degeneracy): D — matches Human Issue #7
- Evan-M12 (Model is SEIRS but called SEIR throughout): C — model labeling error; human did not raise
- Evan-M6b (loglik.se filter threshold of 10 too loose): C — filter too permissive; human did not raise

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 9 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 9 | 7 | 6 | 4 |
| B (AI major, human also found) | 0 | 1 | 1 | 0 |
| C (AI minor, human missed) | 6 | 6 | 9 | 5 |
| D (AI minor, human also found) | 0 | 1 | 1 | 2 |
| E (Human found, AI missed) | 11 | 9 | 9 | 9 |

---

## Per-Reviewer Metrics

**Alex:**
- Human Recall = (B+D) / (B+D+E) = 0 / (0+11) = 0.0%
- AI-Unique Rate = (A+C) / (A+B+C+D) = 15 / 15 = 100.0%

**Charlie:**
- Human Recall = (B+D) / (B+D+E) = 2 / (2+9) = 18.2%
- AI-Unique Rate = (A+C) / (A+B+C+D) = 13 / 15 = 86.7%

**Doug:**
- Human Recall = (B+D) / (B+D+E) = 2 / (2+9) = 18.2%
- AI-Unique Rate = (A+C) / (A+B+C+D) = 15 / 17 = 88.2%

**Evan:**
- Human Recall = (B+D) / (B+D+E) = 2 / (2+11) = 18.2% (wait: B+D+E = 0+2+9 = 11; recall = 2/11 = 18.2%)
- AI-Unique Rate = (A+C) / (A+B+C+D) = 9 / 11 = 81.8%

---

## Cross-Reviewer Aggregation

### Consensus Misses

Human issues that every reviewer (Alex, Charlie, Doug, Evan) failed to cover:

1. Human Issue #1: Too little time spent on the mechanistic POMP model; need thoughtful diagnostics to figure out how science and time series data work coherently.
2. Human Issue #2: MAPE is not comparable between data transformations (unlike log-likelihood which can be adjusted via Jacobian); elaborate modern methods used at expense of appropriate class methods.
3. Human Issue #3: Likelihood is a more efficient inference metric than MAPE; MAPE should also have been calculated for the SEIR model.
4. Human Issue #4: ADF test is inappropriate and a poor choice given clear nonstationarity (diminishing peaks).
5. Human Issue #5: ARMA residual diagnostics incorrectly claim no visible trend/seasonal structure; residuals show extreme heteroskedasticity; log transform needed.
6. Human Issue #8: Mean/median summary statistics are not meaningful for time series with dynamic variation.
7. Human Issue #10: ACF, PACF, and Box-Ljung for ARMA residuals are almost always uninformative after AIC selection; normality check would be more informative.
8. Human Issue #11: The Outlook section appears to be produced by GenAI; modern methods listed without references or details.

Count: 8 out of 11 human issues (72.7%)

### Unique Finds Per Reviewer

A "unique find" is a human issue covered by exactly one reviewer and missed by all others.

- Human Issue #6 (SEIR vs ARMA comparison): covered by Charlie, Doug, and Evan — not unique to any one reviewer.
- Human Issue #7 (particle depletion diagnostics): covered only by Evan (via Evan-NEW-B on ESS monitoring). Unique to Evan.
- Human Issue #9 (Jacobian for ARMA vs log-ARMA): covered by Charlie and Doug — not unique to either.

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 1 |

### Universal AI-Only Flags

Issues raised by every reviewer that the human did not mention:

1. **Pseudo-profile / invalid profile likelihood:** Alex-7, Charlie-3, Doug-5, Evan-M2 all flag that the "profile likelihood" for rho is a scatter plot of global search results, not a proper constrained optimization, and that the CI threshold (maxloglik - 4) is too wide relative to the correct chi-squared value (maxloglik - 1.92).

2. **Mathematical model description vs. implemented code discrepancy (lambda and mu terms):** Alex-6, Charlie-4, Doug-7, Evan-M9 all flag that the written differential equations include a birth/death rate mu and importation term lambda that do not appear in the Csnippet implementation.

3. **SEIRS mislabeled as SEIR throughout:** Alex-3, Charlie-4, Doug-8, Evan-M12 all flag that the model includes waning immunity (omega, R-to-S transitions) making it an SEIRS structure, but the text, equations, and section headers consistently call it SEIR.

Universal AI-only flags count: 3
