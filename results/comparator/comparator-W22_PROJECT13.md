# Comparator Analysis — W22 Project 13

---

## Human Issues

1. Why are initial values treated as known, rather than estimated?

2. The fixed initial value of H does not make sense, but perhaps this does not matter since it gets reset to zero at each observation time.

3. Don't display log likelihood evaluations to 7 decimal places. One is usually enough.

4. The fixed value $\phi=14$ is not explained.

5. For the introduction, it is better to include the background (epidemic situation) in the researched regions, California and Texas.

6. It could be interesting to compare the results for California and Texas, but the report does not make progress on that. Indeed, the report does not put the analysis into the context of the characteristics of the two states analyzed.

7. The visual simulation of local search in California seems to give the wrong value of original daily new cases report in the plot, because the line is the same as the one in Texas. This may be a result of a coding problem where some variable names are re-used for the California and Texas cases.

8. This project builds on previous projects, which is a good thing to do. However, given this helpful start it might have been possible to get further.

9. There is a sign mistake in $\mathrm{Binomial}(S,1-\exp\{\beta \frac{1}{N} \Delta t \})$ which may have been inherited from https://ionides.github.io/531w21/final_project/project15/blinded.html. It is okay to borrow from cited past projects, but one should borrow critically.

10. The results are shown at low computational intensity, for example, only 5 iterations are used to look for the MLE in the local search. Evidently, the group did not learn to take advantage of greatlakes.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "H accumulator/accumvars declaration is in direct conceptual conflict with the factor-of-14 scaling")
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "measurement model contains unexplained fixed scaling factor of 14")
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: covered (matched by finding: "force of infection formula missing the leading negative sign before beta")
- Human Issue #10: covered (matched by finding: "run_level set to 1, giving far-too-small computation settings")

**Findings classification:**
- Finding 1 (global search code absent): A — global search Rmd code entirely missing, making analysis non-reproducible
- Finding 2 (profile likelihood not genuine): A — profile likelihood is filtered global search results, not a proper re-optimization
- Finding 3 (unexplained factor of 14): B — measurement model scaling factor phi=14 never justified (matches Human Issue #4)
- Finding 4 (H accumvars conflict with factor 14): B — H declared as accumvars (reset each step) yet scaled by 14, a direct conceptual conflict (matches Human Issue #2)
- Finding 5 (missing negative sign): B — S-to-E Binomial exponent missing leading minus sign in mathematical writeup (matches Human Issue #9)
- Finding 6 (run_level = 1): B — run_level = 1 yields only 50 particles and 5 MIF iterations, far too small for meaningful inference (matches Human Issue #10)
- Finding 7 (no MIF convergence diagnostic): A — neither local nor global search includes a diagnostic to verify algorithmic convergence
- Finding 8 (Texas params_rw.sd includes nonexistent b3/b4): A — Texas random-walk SD carelessly includes b3 and b4 which do not exist in the Texas model
- Finding 9 (Texas profile CI from global search): C — Texas 95% CI interpreted as valid but derived from inadequate global search coverage of rho
- Finding 10 (eta inconsistency): C — initial susceptible fraction eta=0.01 inconsistent with stated assumption that nearly the entire population is susceptible
- Finding 11 (no ARIMA benchmark): C — no likelihood baseline computed, making it impossible to assess SEIR improvement over a naive model
- Finding 12 (b4 implausibly large): C — b4 initialized at 2000 while MLE converges to ~220, suggesting poor initialization
- Finding 13 (rho described inconsistently): C — rho described as occurring between E and I but actually linked to I-to-R transition in the code
- Finding 14 (strict inequality on date filter): C — strict inequality on both date endpoints may make dataset shorter than claimed
- Finding 15 (covariate table lengths unverified): C — hardcoded covariate interval lengths not checked against actual data row count

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 4 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "Factor-of-14 scaling in measurement model is unjustified for daily data")
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "Lack of quantitative comparison between California and Texas models")
- Human Issue #7: covered (matched by finding: "Texas initial likelihood evaluated with California parameters (code-order bug)")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "Insufficient computation: local search at debugging-level settings")

**Findings classification:**
- Finding 1 (pseudo-profile likelihood): A — profile likelihood is a likelihood slice from global search scatter, not a true optimization over nuisance parameters
- Finding 2 (global search box misaligned): A — lower bound for b4 set at 700 while MLE converges near 221
- Finding 3 (Texas pfilter uses California params): B — code-order bug causes Texas starting-value likelihood to be evaluated with California parameters (matches Human Issue #7)
- Finding 4 (insufficient computation): B — local search run at run_level=1 with 50 particles and 5 iterations (matches Human Issue #10)
- Finding 5 (global search code absent from Rmd): A — reproducibility failure; actual global search computation not present in displayed code
- Finding 6 (no benchmark comparison): A — no non-mechanistic baseline fitted to either state
- Finding 7 (factor-of-14 scaling unjustified): B — phi=14 multiplier borrowed from a weekly-data project, unexplained and distorts parameter interpretation for daily data (matches Human Issue #4)
- Finding 8 (rho described at wrong transition): C — text says reporting occurs at E→I but code accumulates I→R transitions
- Finding 9 (Texas rw.sd specifies extra params): C — b3 and b4 listed in rw.sd but not in Texas model's paramnames
- Finding 10 (tau perturbation effectively zero): C — rw.sd of 0.0001 on log scale effectively fixes tau during filtering
- Finding 11 (fixed epidemiological parameters without sensitivity analysis): C — mu_EI and mu_IR fixed throughout with no sensitivity check
- Finding 12 (no model diagnostics): C — no ESS plots, no conditional log-likelihood plots, no filtering-distribution comparison
- Finding 13 (profile likelihood only for rho): C — contact-rate parameters b1–b4 have no uncertainty quantification despite weak identifiability
- Finding 14 (lack of quantitative comparison between CA and TX): D — no formal comparison of log-likelihoods, contact rates, or reporting rates across states (matches Human Issue #6)
- Finding 15 (policy-effect interpretation not grounded in identifiability): C — conclusion about CDC guideline effect not supported given unquantified identifiability of b3 and b4

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: covered (matched by finding: "H initial value unjustified")
- Human Issue #2: covered (matched by finding: "H initial value unjustified")
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "Fixed Scaling Factor phi=14 Is Unmotivated and Not Estimated")
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed

**Findings classification:**
- Major 1 (Global Search Box Misalignment): A — global search box excludes the true MLE region for both states; all MLE claims invalidated
- Major 2 (Pseudo-Profile): A — profile likelihood constructed from global-search scatter, not genuine constrained optimization
- Major 3 (H Accumulates Recoveries): A — accumulator H tracks dN_IR (recoveries) instead of new infections, creating systematic lag and semantic mismatch
- Major 4 (No Benchmark Comparison): A — no ARIMA or autoregressive baseline provided for comparison with SEIR model
- Major 5 (phi=14 Unmotivated): B — fixed scaling factor phi=14 has no biological justification and is not estimated (matches Human Issue #4)
- Major 6 (Texas Particle Filter Degeneracy): A — Texas local search SE of 12.4 indicates particle filter collapse at initial parameter values
- Major 7 (Global Search Code Missing): A — global search and profile computation code absent from Rmd; results not reproducible
- Major 8 (mu_EI and mu_IR Fixed): A — incubation and recovery rates fixed without sensitivity analysis or uncertainty quantification
- Minor (Notation error mu_SI vs mu_SE): C — text mislabels S-to-E transition rate as mu_SI; code is correct
- Minor (rw.sd for tau effectively zero): C — tau perturbation of 0.0001 prevents meaningful IF2 exploration; effectively fixes tau without declaring it fixed
- Minor (Texas rw.sd spurious b3/b4): C — Texas rw.sd includes b3 and b4 perturbations copied from California despite Texas having only two beta parameters
- Minor (H initial value unjustified): D — H initial values of 613,559 (CA) and 696,761 (TX) are undocumented; but since H resets at each observation time the effect is limited to the first measurement evaluation (matches Human Issues #1 and #2)
- Minor (Cross-state comparisons invalid): C — rho comparison between CA and TX is statistically inappropriate given different model structures
- Minor (No model diagnostics): C — no ESS monitoring, conditional log-likelihoods per period, or residual diagnostics presented
- Minor (Visual-only fit assessment): C — simulation plots before local search constitute only informal model checking with no quantitative fit measure
- Minor (Software version not documented): C — no sessionInfo() or package versions provided

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "C7 — H accumulator initialization")
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "C2 — Unjustified phi=14 scaling parameter")
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "C1 — Critically insufficient mif2 iterations")

**Findings classification:**
- C1: B — Critically insufficient mif2 iterations (~5 iterations, not converged) (matches Human Issue #10)
- C2: B — Unjustified phi=14 scaling parameter, hard-coded, no citation or optimization (matches Human Issue #4)
- C3: A — No non-mechanistic benchmark comparison (ARMA/ARIMA baseline absent)
- C4: A — Texas profile likelihood too noisy to support reliable CI
- C10: A — Policy interpretation (CDC isolation period change) unsupported by unconverged optimization
- C5: C — loglik.se column values unclear (insufficient decimal places or replicate count unspecified)
- C6: C — Run-level computational parameters (NP, NMIF_S, etc.) not documented in manuscript
- C7: D — H accumulator initialization set to large non-zero value, distorting first-step likelihood (matches Human Issue #2)
- C8: C — ESS monitoring and conditional log-likelihood plots absent
- C9: C — Normal measurement model used for count data instead of negative-binomial

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 4 | 4 | 7 | 3 |
| B (AI major, human also found) | 4 | 3 | 1 | 2 |
| C (AI minor, human missed) | 7 | 7 | 7 | 4 |
| D (AI minor, human also found) | 0 | 1 | 1 | 1 |
| E (Human found, AI missed) | 6 | 6 | 7 | 7 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 4 | 0 | 6 | 4/10 = 40% | 4 | 7 | 11/15 = 73% |
| Charlie | 3 | 1 | 6 | 4/10 = 40% | 4 | 7 | 11/15 = 73% |
| Doug | 1 | 1 | 7 | 3/10 = 30% | 7 | 7 | 14/16 = 88% |
| Evan | 2 | 1 | 7 | 3/10 = 30% | 3 | 4 | 7/10 = 70% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #3: Don't display log likelihood evaluations to 7 decimal places. One is usually enough. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #5: For the introduction, it is better to include the background (epidemic situation) in the researched regions, California and Texas. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #8: This project builds on previous projects, which is a good thing to do. However, given this helpful start it might have been possible to get further. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 3 out of 10 human issues (30%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #1: Why are initial values treated as known, rather than estimated? (Covered only by Doug)
- Human Issue #6: It could be interesting to compare the results for California and Texas, but the report does not make progress on that. Indeed, the report does not put the analysis into the context of the characteristics of the two states analyzed. (Covered only by Charlie)
- Human Issue #7: The visual simulation of local search in California seems to give the wrong value of original daily new cases report in the plot, because the line is the same as the one in Texas. This may be a result of a coding problem where some variable names are re-used for the California and Texas cases. (Covered only by Charlie)
- Human Issue #9: There is a sign mistake in $\mathrm{Binomial}(S,1-\exp\{\beta \frac{1}{N} \Delta t \})$ which may have been inherited from https://ionides.github.io/531w21/final_project/project15/blinded.html. It is okay to borrow from cited past projects, but one should borrow critically. (Covered only by Alex)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 1 |
| Charlie | 2 |
| Doug | 1 |
| Evan | 0 |
