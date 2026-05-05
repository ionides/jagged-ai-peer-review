# Ned-Clean Analysis — W22 Project 05

---

## Human Issues

1. Weekly periodicity cannot be described by GARCH.
2. Heteroskedasticity does not explain dependence — heteroskedasticity is about variances, and dependence may be explained by covariances.
3. The ARMA-GARCH model write-up does not explain the model for readers; it would be good to write out the ARMA-GARCH model so readers do not have to track down the reference.
4. Very few replications are carried out for the Monte Carlo inference; such limitations need to be mentioned.
5. Avoid raw, unprocessed R output.
6. The pairs plot is so sparse as to be uninformative; log likelihood does not converge in the local search iterations (only 8 of 20 runs shown, the other 12 produced problematic results), suggesting issues with rmeasure/dmeasure or model design.
7. It would be interesting to see a likelihood comparison between the different models.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "IF2 local search uses only 8 chains regardless of run level")
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "Pairs plots show only 8 local search points — effectively uninformative")
- Human Issue #7: missed

**Findings classification:**
- Primary research question never answered: A — the paper promises counterfactual vaccine simulations but never delivers them
- Critical dmeasure bug (always-true guard): A — `cases >= -10*sd` is always true for non-negative cases, making else branch unreachable
- dmeasure/rmeasure sd formula inconsistency: A — tol placed outside vs. inside sqrt produces different sd values in evaluation vs. simulation
- Model equation errors (V absorbing, E equation uses N_SV instead of N_VE): A — written equations contradict implemented code
- IF2 local search uses only 8 chains: B — too few replications for Monte Carlo inference (matches Human Issue #4)
- Model does not use actual vaccination data despite having it: A — nu treated as fixed constant ignoring observed time-varying vaccination rates
- No profile likelihood or confidence intervals: A — 14 free parameters, no identifiability assessment
- ARMA-GARCH section provides no fitted results (eval=F): A — claimed failure cannot be verified by reader
- beta_t piecewise definition typographical error: C — third condition garbled; label inconsistencies between math and code
- S(0) equation self-referential: C — S(0) appears on both sides; code is correct but math is wrong
- initial_R computed incorrectly (only 6 months of prior cases): C — dramatically understates true recovered population
- Pairs plots show only 8 local search points — effectively uninformative: D — sparse plot uninformative; too few chains (matches Human Issue #6)
- loglik.se < 0.5 filter criterion unjustified: C — nonstandard threshold, no sensitivity analysis
- ARIMA section conflates first differences with second differences: C — exposition unclear about what the model is actually modeling
- Missing model diagram image due to case-sensitivity in filename: C — reproducibility issue on case-sensitive file systems

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "Critically insufficient computation — run_level logic unreliable")
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "No convergence demonstrated for iterated filtering")
- Human Issue #7: covered (matched by finding: "No benchmark comparison")

**Findings classification:**
- Defective dmeasure condition (always-true guard): A — OR condition trivially true; else branch never reached; all log-likelihoods invalid
- Critically insufficient computation — run_level logic unreliable: B — only 8 replicates regardless of run level; too few replications for Monte Carlo inference (matches Human Issue #4)
- No convergence demonstrated for iterated filtering: B — log-likelihood ranges -7000 to -5000 with no upward trend; matches Human Issue #6 (convergence failure, problematic runs)
- No profile likelihoods; no confidence intervals: A — 14 free parameters; identifiability unassessed
- No benchmark comparison: B — ARIMA log-likelihood never compared to POMP on common scale (matches Human Issue #7)
- Stated scientific goal never executed: A — counterfactual vaccine simulations absent
- Model misspecification: E equation adds N_SV instead of N_VE: A — code correct but written math is wrong
- Local search uses mif2 loglik directly without adequate re-evaluation: A — mif2-reported likelihood unreliable due to final-iteration perturbations
- Measurement model Gaussian not epidemiologically justified: A — Gaussian can assign positive probability to negative counts; negative binomial is standard
- Global search box includes fixed parameters silently: A — fragile rbind structure; fixed/estimated not explicitly separated
- rw.sd values halved relative to course standard without justification: C — 0.01 vs. standard 0.02; compounds convergence problem
- S(0) equation circular reference: C — self-referential initial condition; code correct but math wrong
- No model diagnostics (no conditional log-likelihoods, ESS, etc.): C — cannot identify which regime causes convergence failure
- Pairs plot used as substitute for profile likelihood without acknowledgement: C — sparse plots indicate insufficient sampling, not model property
- Multiple spelling and grammatical errors: C — succeptible, Omnicron, preleminary, hetersokadasticity, etc.

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "Computational effort grossly inadequate and reporting incomplete")
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "IF2 convergence failure acknowledged but results presented regardless")
- Human Issue #7: covered (matched by finding: "Complete absence of benchmark comparison")

**Findings classification:**
- Complete absence of benchmark comparison: B — ARIMA log-likelihood never compared to POMP on common scale (matches Human Issue #7)
- IF2 convergence failure acknowledged but results presented regardless: B — log-likelihood waves -7000 to -5000; non-converged results reported as valid inference (matches Human Issue #6)
- Computational effort grossly inadequate and reporting incomplete: B — 8 replicates regardless of run level; 500 particles marginal for 14 parameters; no multi-chain convergence evidence (matches Human Issue #4)
- No profile likelihood or confidence intervals: A — 14 free parameters; pairs plot sparse; identifiability unassessed
- Primary research question never answered: A — vaccine scenario simulations entirely absent
- Measurement model dmeasure always-true condition: A — `cases >= -10*sd` trivially true; else branch dead code
- dmeasure and rmeasure use inconsistent normal parameterizations: A — tol inside vs. outside sqrt produces different sd values
- Global search uses run-level-dependent particle counts with no reported level: A — reader cannot determine whether 50 or 500 particles were used; no Monte Carlo SE reported
- Global search initialization: fixed parameters not explicitly acknowledged: A — six parameters held fixed via single-value runif(1, x, x) without disclosure
- No model diagnostics beyond convergence traces: A — no conditional log-likelihood plots, ESS, or latent state reconstructions
- Compartment model likely typo in E(t) equation: C — N_SV instead of N_VE; code correct but math wrong
- S(0) definition is circular: C — self-referential; code correct but math wrong
- ARIMA model selection ignores weekly seasonality: C — weekly reporting cycles in COVID data unaddressed; only non-seasonal models considered
- ARMA-GARCH failure treated as evidence without diagnostic investigation: C — non-invertible Hessian cause not investigated; inference that POMP is necessary unsupported
- References formatted inconsistently; unprofessional citations: C — Stack Overflow posts and student project URLs cited as sources

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "22.05.5 — Monte Carlo noise in log-likelihood not addressed")
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "22.05.7 — No benchmark comparison")

**Findings classification:**
- 22.05.8 (stated scientific goal not achieved): A — counterfactual vaccine scenario simulations never performed
- 22.05.7 (no benchmark comparison): B — POMP log-likelihoods never compared against ARIMA or any non-mechanistic baseline (matches Human Issue #7)
- 22.05.2/22.05.3 (compartment equation errors: V(t) not subtracting N_VE; S(0) self-referential): A — conservation violated in written equations; code likely correct but math is wrong
- 22.05.6 (no profile likelihoods or parameter confidence intervals): A — no identifiability assessment for any of the 14+ parameters
- 22.05.5 (Monte Carlo noise in log-likelihood not addressed): B — loglik.se up to 0.439 makes parameter ranking unreliable; insufficient pfilter replicates (matches Human Issue #4)
- 22.05.1 (global search underperforms local search without explanation): A — best global loglik (-5677.5) worse than best local (-4796.8) by ~881 units; not acknowledged or investigated
- 22.05.15 (computational parameters not reported): C — Np, Nmif, replicates for each run_level not stated; reproducibility impaired
- 22.05.16 (non-standard measurement model — truncated normal): C — negative binomial is standard for count data; truncated/rounded normal not justified
- 22.05.4 (AIC table non-monotonicity not discussed): C — adding AR terms beyond AR(2) worsens AIC; possible optimization failures not noted
- 22.05.9 (piecewise beta notation inconsistency): C — inconsistent inequality signs at boundary dates
- Notation/typographic errors: C — colloquilly, afformentioned, succeptible, heteroskadasticity, etc.; figure captions absent

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 7 | 7 | 7 | 4 |
| B (AI major, human also found) | 1 | 3 | 3 | 2 |
| C (AI minor, human missed) | 5 | 5 | 5 | 5 |
| D (AI minor, human also found) | 1 | 0 | 0 | 0 |
| E (Human found, AI missed) | 5 | 4 | 4 | 5 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

**Alex**
- Human Recall = (B+D) / (B+D+E) = (1+1) / (1+1+5) = 2/7 = 0.286
- AI-Unique Rate = (A+C) / (A+B+C+D) = (7+5) / (7+1+5+1) = 12/14 = 0.857

**Charlie**
- Human Recall = (B+D) / (B+D+E) = (3+0) / (3+0+4) = 3/7 = 0.429
- AI-Unique Rate = (A+C) / (A+B+C+D) = (7+5) / (7+3+5+0) = 12/15 = 0.800

**Doug**
- Human Recall = (B+D) / (B+D+E) = (3+0) / (3+0+4) = 3/7 = 0.429
- AI-Unique Rate = (A+C) / (A+B+C+D) = (7+5) / (7+3+5+0) = 12/15 = 0.800

**Evan**
- Human Recall = (B+D) / (B+D+E) = (2+0) / (2+0+5) = 2/7 = 0.286
- AI-Unique Rate = (A+C) / (A+B+C+D) = (4+5) / (4+2+5+0) = 9/11 = 0.818

---

## Cross-Reviewer Aggregation

**Consensus misses:** Human issues that every reviewer failed to cover.

- Human Issue #1 (weekly periodicity cannot be described by GARCH): missed by Alex, Charlie, Doug, Evan — 4 out of 4 reviewers.
- Human Issue #2 (heteroskedasticity does not explain dependence): missed by Alex, Charlie, Doug, Evan — 4 out of 4 reviewers.
- Human Issue #3 (ARMA-GARCH model not written out for readers): missed by Alex, Charlie, Doug, Evan — 4 out of 4 reviewers.
- Human Issue #5 (avoid raw unprocessed R output): missed by Alex, Charlie, Doug, Evan — 4 out of 4 reviewers.

Consensus misses: 4 out of 7 human issues (57%).

**Unique finds per reviewer:** Human issues that only one reviewer covered and all others missed.

- Human Issue #4 (very few replications): covered by Alex, Charlie, Doug, Evan — not unique to any single reviewer.
- Human Issue #6 (sparse pairs plot / convergence failure): covered by Alex, Charlie, Doug — not unique.
- Human Issue #7 (likelihood comparison between models): covered by Charlie, Doug, Evan — not unique.

No human issue was covered exclusively by a single reviewer.

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |

**Universal AI-only flags:** Issues raised by every reviewer that the human did not mention.

All four reviewers raised the following issues not found in the human review:

- The stated scientific goal (counterfactual vaccine scenario simulations) was never achieved. (Alex #1, Charlie #6, Doug #5, Evan 22.05.8)
- No profile likelihoods or confidence intervals for any parameter. (Alex #7, Charlie #4, Doug #4, Evan 22.05.6)
- Compartment model equation errors: E(t) equation uses N_SV instead of N_VE; S(0) is self-referential. (Alex #4+#10, Charlie #7+#12, Doug #11+#12, Evan 22.05.2/22.05.3)

Universal AI-only flags: 3 distinct issues raised by all four reviewers and not mentioned by the human.
