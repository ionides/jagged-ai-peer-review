# Ned-Clean Analysis — W22 Project 15

## Human Issues

1. The model is initialized with I=1, which may be inappropriate, possibly biasing parameter estimates and explaining why simulations start slower than the data. Plotting on a log scale would help make this evident.
2. For the delta wave, the I=1 initialization problem is particularly acute, evidenced by noisy likelihood maximization and high noise in simulations.
3. Comparing to a benchmark likelihood (such as log-ARMA) would help identify model misspecification issues.
4. The description k = Initial infecteds does not match the code where k is a measurement overdispersion parameter; similarly N is described as susceptible size but is actually population size.
5. Fixing rho=0.1 is a strong assumption that should be relaxed later.
6. The profile likelihood should be based on a smooth curve from Monte Carlo point estimates, not read directly from noisy points.
7. All these issues together result in a model that gives unstable likelihood evaluation and is hard to filter and hence to obtain maximum likelihood estimates.
8. This project has apparently been carried out independently of all previous STATS/DATASCI 531 projects, which is not entirely an advantage; there is plenty to learn from previous successful projects.
9. Typo in the title "Comparsion" and many other typos may make readers wonder if the numerical work is similarly careless.
10. There should be an explicit link to the data source; reference 4 gives only a website about GISAID's introduction without clear data access instructions.
11. The data has questionable features: cases for both Delta and Omicron become 0 in March 2022, which is inconsistent with known epidemiology, possibly because the initiative stopped classifying cases; without a proper source, this cannot be checked.

---

## Alex

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Initial condition sets I=1 for both variants regardless of scale" — Major #5)
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "Reporting rate fixed without justification for Omicron" — Major #1)
- Human Issue #6: covered (matched by finding: "Profile likelihood for Delta does not cover the MLE, no explanation given" — Major #3)
- Human Issue #7: covered (matched by finding: "Global search Np=2000 severely limiting likelihood accuracy; large SEs" — Major #2)
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed
- Human Issue #11: missed

**Findings classification:**
- Major #1 (rho=0.1 fixed without justification, wave-specific sequencing not considered): B — matches Human Issue #5
- Major #2 (Np=2000 too few particles; loglik.se up to 85; standard practice 20,000+): B — matches Human Issue #7
- Major #3 (Profile for Delta does not cover MLE; CI roughly 100-150, MLE at ~73): B — matches Human Issue #6
- Major #4 (Omicron data filtered to week>40 without justification; time axes non-comparable): A — AI major, human missed
- Major #5 (I=1 initialization biologically implausible, especially for mid-epidemic Omicron): B — matches Human Issue #1
- Major #6 (mu_IR for Delta = 5.46/week = 1.3 days, biologically implausible, not discussed): A — AI major, human missed
- Major #7 (Omicron global search box upper=100, MLE at ~389, box severely too narrow): A — AI major, human missed
- Major #8 (Profile likelihood not plotted on comparable scale; different filtering criteria for each variant): A — AI major, human missed
- Minor #9 (rho fixed but included in partrans with logit transformation — code confusion): C — AI minor, human missed
- Minor #10 (Accumulator H accumulates dN_IR recoveries rather than incidence): C — AI minor, human missed
- Minor #11 (Convergence assessment qualitative and superficial): C — AI minor, human missed
- Minor #12 (guides(color=FALSE) deprecated; c='black' unrecognized argument): C — AI minor, human missed
- Minor #13 (Model does not account for vaccination or waning immunity): C — AI minor, human missed
- Minor #14 (N=300,000,000 questionable for GISAID sequencing data; rho=0.1 implies 30M missed cases/week at Omicron peak): C — AI minor, human missed
- Minor #15 (Nglobal=100 but only two mif2 calls per starting point; second call inherits cooling schedule): C — AI minor, human missed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 4 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Initial Conditions Are Not Fully Justified (I=1, E=0)" — Minor #9)
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "No Non-Mechanistic Benchmark Comparison" — Major #4)
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "Fixed Reporting Rate Is Inappropriate for the Data Source" — Major #1)
- Human Issue #6: covered (matched by finding: "Profile Likelihood for Delta Beta Is Inconsistent with the MLE" — Major #2)
- Human Issue #7: covered (matched by finding: "Large Monte Carlo Standard Errors Undermine Likelihood Comparisons" — Major #5)
- Human Issue #8: missed
- Human Issue #9: covered (matched by finding: "Grammar and Presentation Issues" including 'Comparsion' — Minor #15)
- Human Issue #10: missed
- Human Issue #11: missed

**Findings classification:**
- Major #1 (Fixed Reporting Rate Inappropriate for Data Source; rho=0.1 conflates sequencing fraction with reporting): B — matches Human Issue #5
- Major #2 (Profile Likelihood for Delta Beta Inconsistent with MLE; CI [100,150] does not contain MLE ~73): B — matches Human Issue #6
- Major #3 (Global Search Uses Only One Round of mif2; second call fragile/under-specified): A — AI major, human missed
- Major #4 (No Non-Mechanistic Benchmark Comparison): B — matches Human Issue #3
- Major #5 (Large Monte Carlo SEs undermine likelihood comparisons; loglik.se=5.58; Np=2000): B — matches Human Issue #7
- Major #6 (No Profile Likelihood for mu_EI, mu_IR, or eta; biological conclusions drawn from unidentified parameters): A — AI major, human missed
- Major #7 (Reporting Rate and k Fixed Without Sensitivity Analysis): A — AI major, human missed
- Minor #8 (Delta Trace Plot filters loglik > -2000, hiding non-converging runs): C — AI minor, human missed
- Minor #9 (Initial Conditions Not Fully Justified: I=1, E=0, at mid-epidemic start): D — matches Human Issue #1
- Minor #10 (Omicron Global Search Box Misaligned: Beta upper=100, MLE at 389+): C — AI minor, human missed
- Minor #11 (Profile Beta Range for Delta Does Not Overlap MLE: profile peak ~130, MLE ~73): C — AI minor, human missed
- Minor #12 (mu_IR Biologically Implausible for Delta: 5.46/week ≈ 1.3 days, not flagged): C — AI minor, human missed
- Minor #13 (No Simulation-Based Diagnostics Beyond Visual Overlay; no ESS, no conditional log-likelihood): C — AI minor, human missed
- Minor #14 (Omicron Beta Profile Range Does Not Squarely Include Global MLE; profile max ~350-360 vs MLE ~389): C — AI minor, human missed
- Minor #15 (Grammar and Presentation Issues: 'Comparsion', 'paremetrs', 'inapppropriate', 'causiosly'): D — matches Human Issue #9

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 4 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "No Non-Mechanistic Benchmark Comparison" — Major #5)
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "Reporting Rate Fixed Without Justification" — Major #6)
- Human Issue #6: covered (matched by finding: "Delta Beta Profile Likelihood Collapses to a Singleton CI" — Major #3)
- Human Issue #7: covered (matched by finding: "Global search Np mismatch: Np=20000 local vs Np=2000 global" — Minor)
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed
- Human Issue #11: missed

**Findings classification:**
- Major #1 (Global IF2 Search Initialized from Previous mif2 Result, inheriting terminal cooling schedule): A — AI major, human missed
- Major #2 (Global Search Box Excludes MLE Region for Both Variants; Delta mu_IR and eta outside box; Omicron Beta MLE at 389 vs upper=100): A — AI major, human missed
- Major #3 (Delta Beta Profile Collapses to Singleton CI; only one grid point above cutoff, profile non-smooth): B — matches Human Issue #6
- Major #4 (Global Search Box Excludes Delta MLE for mu_IR; Implausible mu_IR=69.6 at profile peak ≈ 0.1 days): A — AI major, human missed
- Major #5 (No Non-Mechanistic Benchmark Comparison): B — matches Human Issue #3
- Major #6 (Reporting Rate Fixed Without Justification; rho=0.1, no citation, no sensitivity analysis): B — matches Human Issue #5
- Major #7 (Model Diagnostics Are Absent; no ESS, no conditional log-likelihood, no filtering-distribution comparison): A — AI major, human missed
- Major #8 (Parameter Identifiability Not Assessed for mu_EI, mu_IR, eta; biological comparisons drawn without profiles): A — AI major, human missed
- Minor: Global search Np mismatch (Np=20000 local vs Np=2000 global, systematic MC bias): D — matches Human Issue #7
- Minor: k fixed at 10 without justification (high overdispersion expected for COVID surveillance data): C — AI minor, human missed
- Minor: Text incorrectly describes Delta as "most deadly variant" (scientifically misleading framing): C — AI minor, human missed
- Minor: Mixing of time indices across variants (Delta original week; Omicron re-indexed by -40, unexplained): C — AI minor, human missed
- Minor: filter(value>-2000) in local search trace selectively removes non-converging runs: C — AI minor, human missed
- Minor: Simulation plot uses guides(color=FALSE); c='black' unrecognized; observed not distinguished from simulated: C — AI minor, human missed
- Minor: No table comparing parameter estimates across variants: C — AI minor, human missed
- Minor: Log-likelihood comparison across variants not meaningful (different data lengths and magnitudes): C — AI minor, human missed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "No non-mechanistic benchmark comparison" — Major 22.15.4)
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "Reporting rate interpretation; rho=0.1 compound interpretation needs acknowledgment" — Minor 22.15.9)
- Human Issue #6: covered (matched by finding: "Profile likelihood for Delta Beta internally inconsistent; CI does not contain global MLE" — Major 22.15.2)
- Human Issue #7: covered (matched by finding: "Likelihoods not properly evaluated via replicated pfilter; MC variance potentially tens of log-likelihood units" — Major 22.15.1)
- Human Issue #8: missed
- Human Issue #9: covered (matched by finding: "Proofreading; 'Comparsion' and other typos" — Minor 22.15.11)
- Human Issue #10: missed
- Human Issue #11: missed

**Findings classification:**
- 22.15.1 (Likelihoods not properly evaluated via replicated pfilter; single pfilter carries large MC variance): B — matches Human Issue #7
- 22.15.2 (Profile likelihood for Delta Beta internally inconsistent; CI [100,150] does not contain MLE ~73.4): B — matches Human Issue #6
- 22.15.3 (Observation model not specified in Methods; distribution not named): A — AI major, human missed
- 22.15.4 (No non-mechanistic benchmark comparison): B — matches Human Issue #3
- 22.15.5 (Biologically implausible recovery rate for Delta; mu_IR=5.464/week ≈ 1.8 days, not flagged): A — AI major, human missed
- 22.15.6 (ESS not monitored; no particle filter degeneracy check): C — AI minor, human missed
- 22.15.7 (Np and global search iteration count not reported; reproducibility): C — AI minor, human missed
- 22.15.8 (Forward simulation envelopes not distinguished from filtering distribution; envelopes extremely wide): C — AI minor, human missed
- 22.15.9 (Reporting rate rho=0.1; compound interpretation of sequencing and undetected infection rates not acknowledged): D — matches Human Issue #5
- 22.15.10 (Beta labeled "Exposure rate," nonstandard; SEIR diagram lacks equations): C — AI minor, human missed
- 22.15.11 (Proofreading: 'Comparsion', 'paremetrs', 'optimzation', 'causiosly', 'significcant', 'inapppropriate'): D — matches Human Issue #9

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 2 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 4 | 3 | 5 | 2 |
| B (AI major, human also found) | 4 | 4 | 3 | 3 |
| C (AI minor, human missed) | 7 | 6 | 7 | 4 |
| D (AI minor, human also found) | 0 | 2 | 1 | 2 |
| E (Human found, AI missed) | 7 | 5 | 7 | 6 |

---

## Per-Reviewer Metrics

- **Alex:** Human Recall = (B+D)/(B+D+E) = (4+0)/(4+0+7) = 4/11 = **36%** | AI-Unique Rate = (A+C)/(A+B+C+D) = (4+7)/(4+4+7+0) = 11/15 = **73%**
- **Charlie:** Human Recall = (B+D)/(B+D+E) = (4+2)/(4+2+5) = 6/11 = **55%** | AI-Unique Rate = (A+C)/(A+B+C+D) = (3+6)/(3+4+6+2) = 9/15 = **60%**
- **Doug:** Human Recall = (B+D)/(B+D+E) = (3+1)/(3+1+7) = 4/11 = **36%** | AI-Unique Rate = (A+C)/(A+B+C+D) = (5+7)/(5+3+7+1) = 12/16 = **75%**
- **Evan:** Human Recall = (B+D)/(B+D+E) = (3+2)/(3+2+6) = 5/11 = **45%** | AI-Unique Rate = (A+C)/(A+B+C+D) = (2+4)/(2+3+4+2) = 6/11 = **55%**

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- **Human Issue #2:** For the delta wave, the I=1 initialization problem is particularly acute, evidenced by noisy likelihood maximization and high noise in simulations.
- **Human Issue #4:** The description k = Initial infecteds does not match the code where k is a measurement overdispersion parameter; similarly N is described as susceptible size but is actually population size.
- **Human Issue #8:** This project has apparently been carried out independently of all previous STATS/DATASCI 531 projects, which is not entirely an advantage; there is plenty to learn from previous successful projects.
- **Human Issue #10:** There should be an explicit link to the data source; reference 4 gives only a website about GISAID's introduction without clear data access instructions.
- **Human Issue #11:** The data has questionable features: cases for both Delta and Omicron become 0 in March 2022, which is inconsistent with known epidemiology, possibly because the initiative stopped classifying cases; without a proper source, this cannot be checked.

**Count: 5 out of 11 human issues were missed by every reviewer.**

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- **Alex only:** Human Issue #1 (I=1 initialization inappropriate) — Alex covered via Major #5; Charlie covered via Minor #9; neither Doug nor Evan covered it. Actually, both Alex and Charlie covered #1, so it is not unique to Alex. Let me re-examine each issue.

  Human Issue #1: Alex=covered, Charlie=covered, Doug=missed, Evan=missed. Not unique.
  Human Issue #3: Alex=missed, Charlie=covered, Doug=covered, Evan=covered. Not unique.
  Human Issue #5: Alex=covered, Charlie=covered, Doug=covered, Evan=covered. Not unique.
  Human Issue #6: Alex=covered, Charlie=covered, Doug=covered, Evan=covered. Not unique.
  Human Issue #7: Alex=covered, Charlie=covered, Doug=covered, Evan=covered. Not unique.
  Human Issue #9: Alex=missed, Charlie=covered, Doug=missed, Evan=covered. Not unique.

No human issue was covered by exactly one reviewer.

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |

### Universal AI-only flags

Issues raised by every reviewer that the human did not mention:

- Every reviewer raised the **profile likelihood inconsistency / unreliability** (Alex Major #3, Charlie Major #2, Doug Major #3, Evan Major 22.15.2). However, this was matched to Human Issue #6 for all reviewers (B), so it is not an AI-only flag.
- Every reviewer raised the **no benchmark comparison** issue (matched to Human Issue #3 for Charlie, Doug, Evan; missed by Alex). Not universal AI-only.
- Every reviewer raised concerns about **rho=0.1** (matched to Human Issue #5). Not universal AI-only.

Looking for findings that all four reviewers raised AND that the human did not mention:

- **Biologically implausible mu_IR for Delta** (Alex Major #6, Charlie Minor #12, Doug Major #4, Evan Major 22.15.5): All four reviewers raised this. Human did not raise it. Universal AI-only flag.
- **Profile-related internal inconsistency details beyond smooth curve**: Alex Major #8 (asymmetric profile filtering), Charlie Minor #11 (Delta profile peak vs MLE discrepancy), Doug Major #3 (singleton CI), Evan 22.15.2 — these are all about the profile but in different specifics; the human only raised the smooth-curve issue, so all the deeper profile analysis details are AI-only but not uniformly shared.

Universal AI-only finds (raised by all four reviewers, human did not raise):
1. **Biologically implausible mu_IR for Delta** (mu_IR = 5.46/week ≈ 1.3 days, inconsistent with COVID infectious period of 5-10 days, not discussed): Alex Major #6 / Charlie Minor #12 / Doug Major #4 / Evan Major 22.15.5.

**Count: 1 universal AI-only flag.**
