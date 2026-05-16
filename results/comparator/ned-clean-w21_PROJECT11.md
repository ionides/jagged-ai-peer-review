# Ned-Clean Analysis — W21 Project 11

---

## Human Issues

1. The shaded region around the trend line in Section 2 is unexplained — is it meaningful in this situation?
2. The Augmented Dickey-Fuller (ADF) test is not particularly appropriate here, since the null hypothesis of an ARMA model is not of interest for COVID data.
3. If nonstationarity is concluded from ADF or similar, fitting a stationary model is not a natural next step.
4. The POMP model is written as an ODE system even though it is not one.
5. Simulations show much higher variability in the data than in the model simulations, which follow a smooth curve with little stochasticity — a warning sign about the model.
6. The perturbed model obtains log-likelihoods around -300 but these deteriorate as perturbations decrease; this is likely due to insufficient process/measurement noise; binomial measurement is problematic (bounded support, cannot fit overdispersion); no additional noise in rates.
7. Effective sample size is often close to zero, another indication of insufficient stochasticity.
8. The project mentions trying models with additional variability but does not carry it out; for a 5-person group, this could have been delegated.
9. References should follow a standard format with bibliographic metadata, not just links.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "Extremely Poor Log-Likelihood Values — Model Fit Is Catastrophically Bad")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed

**Findings classification:**
- Finding 1 (H accumulator initialized to (1-eta)*N): A — Major; H initialization error not raised by human
- Finding 2 (Measurement model binomial misapplied — H tracks I→R not E→I): A — Major; measurement model semantic error not raised by human
- Finding 3 (No profile likelihood or CIs): A — Major; profile likelihood absence not raised by human
- Finding 4 (Extremely poor log-likelihoods, catastrophically bad model fit): B — Major; matches Human Issue #6 (log-likelihoods deteriorate, model lacks stochasticity)
- Finding 5 (logit transform on Beta invalid): A — Major; parameter transformation error not raised by human
- Finding 6 (Global search mif2 re-run without adequate cooling): A — Major; global search setup issue not raised by human
- Finding 7 (External URL dependency breaks reproducibility): A — Major; data reproducibility issue not raised by human
- Finding 8 (Two different data streams used for ARMA and POMP): C — Moderate (treated as Minor); data stream inconsistency not raised by human
- Finding 9 (HP filter lambda=100 inappropriate for daily data): C — Moderate (treated as Minor); HP filter lambda not raised by human
- Finding 10 (rho fixed at 0.1 without sensitivity analysis): C — Moderate (treated as Minor); rho fixed not raised by human
- Finding 11 (E(0) and I(0) hard-coded without uncertainty): C — Moderate (treated as Minor); initial conditions not raised by human
- Finding 12 (Convergence diagnostics incomplete and narrative out of order): C — Moderate (treated as Minor); convergence diagnostics not raised by human
- Finding 13 (ARMA model selection poorly justified; ARMA(1,1) printed but ARMA(2,2) chosen): C — Moderate (treated as Minor); ARMA code-text inconsistency not raised by human
- Finding 14 (Weekly seasonality noted but not addressed): C — Minor; weekly seasonality not raised by human
- Finding 15 (No simulation-based model check after fitting): C — Minor; no posterior predictive simulation not raised by human

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
- Human Issue #6: covered (matched by finding: "Very large Monte Carlo standard errors in reported likelihoods")
- Human Issue #7: covered (matched by finding: "No model diagnostics — ESS, conditional log-likelihoods, filtering distribution")
- Human Issue #8: missed
- Human Issue #9: missed

**Findings classification:**
- Finding 1 (Accumulator H accumulates recoveries not new cases): A — Major; measurement model semantic error not raised by human
- Finding 2 (Reporting rate rho and eta fixed rather than estimated): A — Major; parameter fixing not raised by human
- Finding 3 (No profile likelihoods computed): A — Major; profile likelihood absence not raised by human
- Finding 4 (Global search uses too little computational effort): A — Major; global search effort not raised by human
- Finding 5 (No non-mechanistic benchmark comparison): A — Major; benchmark comparison not raised by human
- Finding 6 (Very large MC standard errors in reported likelihoods): B — Major; matches Human Issue #6 (log-likelihoods deteriorate, insufficient stochasticity)
- Finding 7 (mu_EI convergence to zero = model misspecification): A — Major; mu_EI convergence interpretation not raised by human
- Finding 8 (No model diagnostics — conditional log-likelihoods, ESS, filtering distribution): B — Major; matches Human Issue #7 (ESS close to zero, insufficient stochasticity indicator)
- Finding 9 (rw.sd magnitudes too small): C — Minor; rw.sd magnitudes not raised by human
- Finding 10 (HP filter lambda not appropriate for daily data): C — Minor; HP filter lambda not raised by human
- Finding 11 (Convergence diagnosis focuses on parameter spread not likelihood stability): C — Minor; convergence diagnosis priority not raised by human
- Finding 12 (Global search description appears before code): C — Minor; narrative ordering not raised by human
- Finding 13 (partrans omits eta from transformation): C — Minor; partrans omission not raised by human
- Finding 14 (Data loaded from remote GitHub URL): C — Minor; URL dependency not raised by human
- Finding 15 (No simulation-based diagnostics vs. forward simulations): C — Minor; simulation diagnostics not raised by human

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 2 |
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
- Human Issue #6: covered (matched by finding: "Insufficient computational effort; Monte Carlo standard errors too large")
- Human Issue #7: covered (matched by finding: "No model diagnostics — conditional log-likelihoods, ESS, filtering distribution")
- Human Issue #8: missed
- Human Issue #9: missed

**Findings classification:**
- Finding 1 (Accumulator variable accumulates recoveries not new reported cases): A — Major; measurement model semantic error not raised by human
- Finding 2 (Smoothed 7-day rolling average fed to binomial measurement model): A — Major; smoothed data in measurement model not raised by human
- Finding 3 (Global search initialized from previous mif2 result, not base pomp object): A — Major; global search initialization error not raised by human
- Finding 4 (No quantitative benchmark comparison): A — Major; benchmark comparison not raised by human
- Finding 5 (No profile likelihoods; identifiability not assessed): A — Major; profile likelihood absence not raised by human
- Finding 6 (Insufficient computational effort; MC SEs too large): B — Major; matches Human Issue #6 (log-likelihoods deteriorate, insufficient stochasticity)
- Finding 7 (mu_EI convergence to zero = model misspecification, not biological finding): A — Major; mu_EI convergence interpretation not raised by human
- Finding 8 (No model diagnostics — ESS, conditional log-likelihoods, filtering distribution): B — Major; matches Human Issue #7 (ESS close to zero)
- Finding 9 (rho fixed without justification or sensitivity analysis): A — Major; rho fixed not raised by human
- Finding 10 (HP filter lambda not appropriate for daily data): C — Minor; HP filter lambda not raised by human
- Finding 11 (ARMA fitted to HP-filtered; POMP fitted to smoothed counts — comparison invalid): C — Minor; ARMA-POMP comparison invalidity not raised by human
- Finding 12 (Data loaded from GitHub URL — reproducibility dependency): C — Minor; URL dependency not raised by human
- Finding 13 (partrans declares logit for Beta, mu_EI, mu_IR but not eta): C — Minor; partrans omission not raised by human
- Finding 14 (No forecast or policy-relevant prediction from fitted SEIR): C — Minor; forecast absence not raised by human
- Finding 15 (Initial conditions E(0) and I(0) fixed, not estimated): C — Minor; initial condition estimation not raised by human

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 0 |
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
- Human Issue #6: covered (matched by finding: "21.11.2 — Log-likelihood optimum based on single unreplicated pfilter evaluation")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: covered (matched by finding: "Presentation — reference list non-functional")

**Findings classification:**
- 21.11.1 (H initialization error corrupts measurement model): A — Major; H initialization error not raised by human
- 21.11.2 (Log-likelihood optimum from single unreplicated pfilter): B — Major; matches Human Issue #6 (log-likelihoods unreliable, model lacks stochasticity)
- 21.11.4 (No quantitative benchmark comparison ARMA vs. SEIR): A — Major; benchmark comparison not raised by human
- 21.11.5 (rho fixed at 0.1 without estimation or profile likelihood): A — Major; rho fixed not raised by human
- 21.11.6 (No profile likelihoods or CIs for any free SEIR parameter): A — Major; profile likelihood absence not raised by human
- 21.11.CON (Population conservation violated at initialization): C — Minor; population conservation not raised by human
- 21.11.7 (eta not included in logit parameter transformation): C — Minor; partrans omission not raised by human
- 21.11.8 (HP filter lambda = 100 inappropriate for daily data): C — Minor; HP filter lambda not raised by human
- 21.11.9 (Weekly periodicity in ARMA residuals not addressed): C — Minor; weekly seasonality not raised by human
- 21.11.3 (Confusing: ARMA(1,1) output shown in ARMA(2,2) section): C — Minor; ARMA code-text inconsistency not raised by human
- Presentation (Reference list non-functional — only "here" as URL text): D — Minor; matches Human Issue #9 (references should have bibliographic metadata)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 6 | 6 | 7 | 4 |
| B (AI major, human also found) | 1 | 2 | 2 | 1 |
| C (AI minor, human missed) | 8 | 7 | 6 | 5 |
| D (AI minor, human also found) | 0 | 0 | 0 | 1 |
| E (Human found, AI missed) | 8 | 7 | 7 | 7 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

**Human Recall** = (B + D) / (B + D + E)

- Alex: (1 + 0) / (1 + 0 + 8) = 1/9 = 0.111 (11.1%)
- Charlie: (2 + 0) / (2 + 0 + 7) = 2/9 = 0.222 (22.2%)
- Doug: (2 + 0) / (2 + 0 + 7) = 2/9 = 0.222 (22.2%)
- Evan: (1 + 1) / (1 + 1 + 7) = 2/9 = 0.222 (22.2%)

**AI-Unique Rate** = (A + C) / (A + B + C + D)

- Alex: (6 + 8) / (6 + 1 + 8 + 0) = 14/15 = 0.933 (93.3%)
- Charlie: (6 + 7) / (6 + 2 + 7 + 0) = 13/15 = 0.867 (86.7%)
- Doug: (7 + 6) / (7 + 2 + 6 + 0) = 13/15 = 0.867 (86.7%)
- Evan: (4 + 5) / (4 + 1 + 5 + 1) = 9/11 = 0.818 (81.8%)

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues missed by every reviewer (all of Alex, Charlie, Doug, Evan):

- Human Issue #1: Unexplained shaded region around trend line in Section 2
- Human Issue #2: ADF test not appropriate — null hypothesis of ARMA model not of interest
- Human Issue #3: Concluding nonstationarity then fitting a stationary model is illogical
- Human Issue #4: POMP model written as an ODE system even though it is not one
- Human Issue #5: Data variability much higher than simulations — warning sign of insufficient stochasticity
- Human Issue #8: Project mentions trying additional variability but does not carry it out

**Count: 6 out of 9 human issues (66.7%) were missed by every reviewer.**

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #9 (references need bibliographic metadata): covered only by **Evan** (via "Presentation" finding); missed by Alex, Charlie, Doug.
- Human Issue #6 (log-likelihoods deteriorate; insufficient stochasticity): covered by Alex, Charlie, Doug, and Evan — not a unique find.
- Human Issue #7 (ESS close to zero): covered by Charlie and Doug — not a unique find.

Summary of unique finds:

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 1 |

### Universal AI-only flags

Issues raised as Major by every reviewer that the human did not mention:

- Measurement model error: accumulator H accumulates I→R transitions (recoveries) instead of E→I transitions (new cases) — raised as Major by Alex (finding 2), Charlie (finding 1), Doug (finding 1), Evan (21.11.1). All four reviewers flagged this as a critical code-level bug not addressed by the human.
- No profile likelihoods computed for any parameter — raised as Major by Alex (finding 3), Charlie (finding 3), Doug (finding 5), Evan (21.11.6).
- No quantitative benchmark comparison — raised as Major by Charlie (finding 5), Doug (finding 4), Evan (21.11.4); raised implicitly by Alex (finding 4 covers poor likelihoods but not the benchmark framing explicitly). Three of four reviewers raised it as Major.
- rho fixed at 0.1 without estimation or sensitivity analysis — raised as Major/Moderate by Charlie (finding 2), Doug (finding 9), Evan (21.11.5); raised as Moderate by Alex (finding 10).

**Universal AI-only Major flags (all four reviewers): 2**
1. Measurement model semantic error (H accumulates recoveries, not new cases)
2. No profile likelihoods computed
