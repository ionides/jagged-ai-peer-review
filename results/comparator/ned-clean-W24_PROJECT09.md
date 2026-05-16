# Ned-Clean Analysis — W24 Project 09

---

## Human Issues

1. Too much unformatted and undescribed R output; figure numbers and captions would help.
2. ARMA modeling is known to be a poor choice for financial markets, so may not be worth much space; the many ARMA figures are unexplained and don't contribute much.
3. ARMA-GARCH may be less well motivated than t-GARCH; the latter can fit long tails (which are present) and does not attempt to explain autocorrelations (which are expected to be small anyway, per the efficient market hypothesis).
4. It is interesting to investigate the possibility of simplifying the leverage model — that is the sort of analysis the flexibility of the POMP model class permits.
5. The ARMA(5,5) inverse roots are essentially on the unit circle, indicating numerical instability; concluding this is a good, stable model is wrong; there is no point making diagnostic plots if you ignore the problems they reveal.
6. The decreasing likelihood through the search iterations suggests model misspecification: the noise in the parameters included for the parameter search is needed to explain the data.
7. The global search has not converged; H_0 continues to decrease.
8. The code variable sigma_eta is not explained in the mathematical description of the model.
9. When phi=1, the model has singular behavior (sigma^2_{w,n}=0 for all choices of sigma_eta and G); values close to phi=1 occur often; this problem may explain some weird convergence diagnostic plots.

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

**Findings classification:**
- Issue 1 (Profile likelihood code bug): A — profile uses if.box[[i]] instead of if.prof[[i]], invalidating the CI
- Issue 2 (Likelihood comparison invalid across models): A — ARIMA, GARCH, and POMP log-likelihoods not directly comparable
- Issue 3 (Insufficient computational effort for 13,000-obs dataset): A — Np=2000 likely too few particles; no ESS diagnostics
- Issue 4 (Profile initializes from wrong starting point): A — profile loop starts from if1[[1]] not guesses[i,]
- Issue 5 (No simulation-based model checking for POMP): A — no posterior predictive check for full Breto model
- Issue 6 (No formal LRT between Breto and no-leverage): A — nested comparison lacks formal test or AIC adjustment
- Issue 7 (Global search box bounds implausibly wide): A — sigma_eta upper bound of 60 is physically unreasonable
- Issue 8 (Inconsistency in fGarch log-likelihood values in text): C — text reports values that differ from rendered output
- Issue 9 (ACF on demeaned returns rather than squared): C — ACF of raw returns uninformative for volatility clustering
- Issue 10 (Local search uses single starting point): C — all mif2 chains start from same params_test vector
- Issue 11 (run_level silently reduced to 2 for no-leverage model): C — simplified model run at much lower computational effort with no explanation
- Issue 12 (Initial pfilter test on simulated data not real data): C — pfilter applied to sim1.filt, not ndx.filt
- Issue 13 (No convergence diagnostics for profile likelihood): C — no trace or pair plots for if.prof runs
- Issue 14 (Definition of sigma_w^2 not verified or connected): C — parameterization difference between the two models not discussed
- Issue 15 (Conclusion mischaracterizes profile likelihood result): C — calling flawed profile output "validation" overstates finding

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 9 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "No Benchmark Comparison Against Standard GARCH Baseline — t-distributed innovations not considered")
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "ARIMA Analysis Selects ARMA(5,5) Incorrectly — near-unit-circle roots noted")
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: covered (matched by finding: "Stochastic Volatility Model Not Described with Adequate Mathematical Precision")
- Human Issue #9: missed

**Findings classification:**
- Issue 1 (Profile likelihood code bug): A — if.box[[i]] used instead of if.prof[[i]]
- Issue 2 (GARCH and POMP likelihoods not comparable): A — different parameterization, observation count, and optimization precision
- Issue 3 (Insufficient computational effort for 13,000-obs dataset): A — Np=2000 may cause particle degeneracy; no ESS diagnostics
- Issue 4 (Profile initializes from if1[[1]] not guesses): A — starting-value diversity not utilized in profile optimization
- Issue 5 (No benchmark comparison / t-distributed innovations): B — explicitly asks whether t-GARCH was considered (matches Human Issue #3)
- Issue 6 (Simplified model comparison methodologically flawed): A — run_level=2 vs run_level=3 confounds computational effort with model structure
- Issue 7 (No model diagnostics beyond trace plots): A — no ESS, no conditional log-likelihood, no simulation-based checks
- Issue 8 (Initial conditions fixed and not estimated): C — sensitivity to G_0 and H_0 initialization not assessed
- Issue 9 (Inconsistent run_level for simplified model): C — silent reset to run_level=2 not explained
- Issue 10 (Log-likelihood threshold hardcoded): C — hardcoded 43483 threshold may not match actual maximum on re-run
- Issue 11 (ARIMA selects ARMA(5,5) incorrectly): D — notes AIC anomaly and near-unit-circle roots (matches Human Issue #5)
- Issue 12 (Missing sessionInfo()): C — package versions not pinned; reproducibility concern
- Issue 13 (Archived .rda files not provided): C — readers cannot verify results without re-running expensive computation
- Issue 14 (Mathematical precision insufficient): D — sigma_eta role not clearly explained; code-math mismatch possible (matches Human Issue #8)
- Issue 15 (Minor writing and notation issues): C — typos and circular conclusion statement

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "No-leverage model comparison — t-distributed innovations not considered as baseline")
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "ARIMA AIC table anomaly — near-unit-circle roots flagged")
- Human Issue #6: covered (matched by finding: "Convergence not adequately demonstrated — loglik decreases after peaking")
- Human Issue #7: missed
- Human Issue #8: covered (matched by finding: "Inconsistent notation — sigma_n undefined in math description")
- Human Issue #9: missed

**Findings classification:**
- Issue 1 (Initial pfilter on simulated data not real data): A — log-likelihood of ~-17965 computed against sim data, not NASDAQ returns
- Issue 2 (Global IF2 search initialized from previous mif2 result): A — if.box inherits near-zero perturbation magnitude from if1[[1]]
- Issue 3 (Profile likelihood uses wrong parameter source): A — coef(if.box[[i]]) used instead of coef(if.prof[[i]])
- Issue 4 (Invalid cross-model log-likelihood comparison): A — GARCH and POMP likelihoods differ in parameterization and observation model
- Issue 5 (No-leverage comparison computationally unfair / t-GARCH not considered): B — explicitly mentions t-distributed innovations as missing baseline (matches Human Issue #3)
- Issue 6 (Convergence not demonstrated; loglik decreases): B — trace shows loglik increases then decreases; matches misspecification signal (matches Human Issue #6)
- Issue 7 (ARIMA AIC table anomaly): B — flags near-unit-circle roots; ARMA(5,5) anomalous AIC (matches Human Issue #5)
- Periodogram frequency units (minor): C — peak frequency not converted to interpretable cycles-per-year
- Text vs output table misstatement (minor): C — narrative figures differ from rendered HTML output
- Inconsistent notation — sigma_n undefined (minor): D — sigma_n in math description undefined; code uses sigma_eta (matches Human Issue #8)
- sigma_nu converging to zero not interpreted (minor): C — G process may be unidentifiable but not flagged
- Missing CI for leverage vs. no-leverage (minor): C — LRT not performed for the 203 log-likelihood unit difference
- timing.box assignment error (minor): C — .system.time artifact may be out of scope
- No model diagnostics for POMP model (minor): C — no ESS trace, no conditional log-likelihood, no simulation comparison
- Data mislabeling NASDAQ 100 vs Composite (minor): C — ^IXIC is the Composite, not NASDAQ 100

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 6 |
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
- Human Issue #5: covered (matched by finding: "AIC table anomaly for ARMA(5,5) — near-unit-circle roots suggested")
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "Convergence not achieved for phi and mu_h — global search not consistent")
- Human Issue #8: missed
- Human Issue #9: missed

**Findings classification:**
- 24.09.1 (AIC table anomaly for ARMA(5,5)): B — flags -79185.97 as anomalous; suggests checking near-unit-circle roots (matches Human Issue #5)
- 24.09.3/24.09.2 (Monte Carlo variability / mif2 likelihood interpretation): A — mif2-internal likelihood is perturbed and not a valid estimate for model comparison
- 24.09.5 (Profile likelihood too sparse for reliable CI): A — few profile points; particle filter SE non-negligible relative to chi-squared threshold
- 24.09.6 (Convergence not achieved for phi and mu_h): B — trace plots show wide parameter ranges; global optimizer not consistent (matches Human Issue #7)
- 24.09.4 (Likelihood comparability between GARCH and POMP): A — fGARCH vs tseries discrepancy not explained; observation model alignment not verified
- Notation inconsistency (sigma_{w,n} vs sigma_w) (minor): C — difference between full and simplified model notation not explained
- Ljung-Box test for model selection (minor): C — less preferred than AIC-based selection
- ESS not monitored (minor): C — particle filter effective sample size never mentioned
- No summary comparison table (minor): C — log-likelihood and parameter count table would improve readability
- Run level parameters (minor): C — run level settings stated inline, not in consolidated specification
- sigma_w^2 structural constraint (minor): C — parameterization choice not justified
- Strogatz citation (minor): C — not connected to any methodological claim
- Proofreading (minor): C — multiple typos throughout manuscript

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 7 | 6 | 4 | 3 |
| B (AI major, human also found) | 0 | 1 | 3 | 2 |
| C (AI minor, human missed) | 8 | 5 | 6 | 8 |
| D (AI minor, human also found) | 0 | 2 | 1 | 0 |
| E (Human found, AI missed) | 9 | 6 | 5 | 7 |

---

## Per-Reviewer Metrics

| Reviewer | Human Recall (B+D)/(B+D+E) | AI-Unique Rate (A+C)/(A+B+C+D) |
|----------|---------------------------:|--------------------------------:|
| Alex | 0/9 = 0.00 | 15/15 = 1.00 |
| Charlie | 3/9 = 0.33 | 11/14 = 0.79 |
| Doug | 4/9 = 0.44 | 10/14 = 0.71 |
| Evan | 2/9 = 0.22 | 11/13 = 0.85 |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover (missed by Alex, Charlie, Doug, and Evan):

1. Human Issue #1: Too much unformatted and undescribed R output; figure numbers and captions would help.
2. Human Issue #2: ARMA modeling is known to be a poor choice for financial markets; the many ARMA figures are unexplained.
4. Human Issue #4: Investigating the possibility of simplifying the leverage model is a valuable use of the POMP model class.
9. Human Issue #9: When phi=1, the model has singular behavior; values close to phi=1 occur often and may explain convergence issues.

Count: 4 out of 9 human issues (4/9 = 44%)

### Unique finds per reviewer

Issues covered by exactly one reviewer and missed by all others:

- Human Issue #6 (decreasing likelihood suggests model misspecification): covered only by **Doug** (Major Issue 6)
- Human Issue #7 (global search not converged; H_0 continues to decrease): covered only by **Evan** (Major 24.09.6)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 1 |
| Evan | 1 |

### Universal AI-only flags

Issues raised by every reviewer (as major or minor) that the human did not mention:

1. **GARCH and POMP log-likelihood comparison is invalid or not formally justified** — raised by all four reviewers (Alex Major 2, Charlie Major 2, Doug Major 4, Evan Major 24.09.4). All note that GARCH and POMP likelihoods differ in parameterization, observation model, or computational precision and cannot be directly compared without adjustment.

2. **No model diagnostics / simulation-based checks beyond trace plots** — raised by all four reviewers (Alex Major 5, Charlie Major 7, Doug Minor "No model diagnostics for POMP model", Evan Minor "ESS not monitored"). All note the absence of ESS monitoring, conditional log-likelihood per time step, or simulation-based model checking for the full Breto model.

Universal AI-only count: 2
