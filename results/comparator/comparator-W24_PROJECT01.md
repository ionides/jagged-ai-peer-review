# Comparator Analysis — W24 Project 01

---

## Human Issues

1. The dataset must somehow determine whether an election is free and fair, since many autocracies claim to have a democratic mandate. A brief explanation would help the reader.

2. Is there an error in Fig. 1? $Z(t)$ seems to be defined as non-negative. It is unusual to require $\Delta(Z(t))$ to be non-negative.

3. The diagram is written with $S$ as a compartment, and in the Csnippet the value of `S` changes dynamically. For a covariate, the value would be data. New sovereign states entering $S$ could be considered as a covariate process, analogous to birth/immigration in an epidemic model.

4. $\Delta Z(t)$ is described as the number of democracies, but is it actually the change in that number? Perhaps the plot of the graphs for $Z(t)$ and $\Delta Z(t)$ seem incorrectly labeled. The graph on the right looks like the differences of the $Z(t)$ values, without performing the transform defined for $\Delta Z(t)$, while the graph on the left aligns more with the newly defined $\Delta Z(t)$, the positive change of new democratic states.

5. From the measurement model, it is clear that $N$ counts democracies. But, the model does not let states return from democracy to autocracy?

6. The $P$ and $R$ components are not clearly defined. $P$ should maybe be defined as the change in the number of states that are still under the control of powerful elites who are for the current state. Then the states that are under heavy influence of the elites would then transition to state $R$, which is the change in the number of states that enter a revolution, or revolution is threatened. The way the model is defined leaves me to believe that there should be a state after $N$, which would be the final compartment for states that achieve democracy, instead of remaining in negotiations, or going back to revolution. The variables $\beta$ and $R(t)$ are introduced, and while $R(t)$ is previously defined, $\beta$ isn't given a definition, so at this point, no intuition is given as to what this variable represents.

7. In Fig. 4, $\beta$ and $\mu_{PR}$ plots would be clearer with the x-axis on a log scale.

8. Fig. 7. The "moderate evidence" has p-values well above the usual evidence requirements. It is still okay to comment on small and statistically insignificant effects, but this needs explanation.

9. Section 2.2. Fig. 2 is explained to show that the parameter estimated are well identified, but some combinations of them seem weakly identified, for example the nonlinear trade-off between $\mu_{RN}$ and $\rho$.

10. In the profile, $k$ is not identifiable as it has values across its whole range that maximize the likelihood. It is nice that the project created several profiles of different parameters.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "ΔZ(t) truncation — measurement model ignores left-censoring at zero")
- Human Issue #3: covered (matched by finding: "S treated as compartment but also used as covariate — model internally inconsistent")
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "N accumulates monotonically but is never depleted — model cannot capture democratic decline")
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: covered (matched by finding: "probe results interpretation contradictory — 'moderate evidence' of misfit then claimed as reliability")
- Human Issue #9: covered (matched by finding: "negative exponential relationship in pair plot attributed to theory but is symptom of parameter confounding")
- Human Issue #10: missed

**Findings classification:**
- Finding 1 (No mif2 code shown): A — algorithm identity and reproducibility cannot be verified
- Finding 2 (Global search, not profile likelihood): A — CI construction invalid; profiles not computed by optimizing out nuisance parameters
- Finding 3 (Transition rate contradicts model equation): A — code uses N/tot_sov, equation states β·R(t)/ζ(t); three-way mismatch
- Finding 4 (ΔZ(t) truncation, measurement model ignores left-censoring): B — matches Human Issue #2
- Finding 5 (S as compartment and covariate simultaneously): B — matches Human Issue #3
- Finding 6 (N accumulates monotonically, never depleted): B — matches Human Issue #5
- Finding 7 (AIC for IID model computed incorrectly): A — formula uses 2 instead of 4 parameters
- Finding 8 (Poisson log-likelihood hard-coded): A — non-reproducible literal value rather than logLik() extraction
- Finding 9 (No convergence diagnostics): C — no trace plots, no multi-run comparison
- Finding 10 (Figure caption numbering incorrect): C — Fig. 3 labeled "Figure 2," Fig. 7 used twice
- Finding 11 (Probe results interpretation contradictory): D — matches Human Issue #8
- Finding 12 (Negative exponential relationship interpretation unsupported): D — matches Human Issue #9
- Finding 13 (rho interpreted as "coding efficiency"): C — non-standard reinterpretation of reporting fraction without justification
- Finding 14 (Initial condition for S inconsistent with data): C — S(0)=23 with P(0)+R(0)+N(0)=4 lacks justification
- Finding 15 (Poisson log-likelihood stated without derivation): C — same underlying reproducibility issue as Finding 8; no code path shown

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 5 |
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
- Human Issue #8: covered (matched by finding: "Probe interpretation is overly optimistic")
- Human Issue #9: covered (matched by finding: "Claim of 'well identified' parameters is unsupported")
- Human Issue #10: contradiction (Charlie says these are not profiles at all; human says "it is nice that the project created several profiles")

**Findings classification:**
- Major 1 (Model-code inconsistency in S→P transition rate — code uses N/tot_sov instead of R/S): A
- Major 2 (Measurement model maps cumulative state N to annual flow observation): A
- Major 3 (Compartment conservation violation at initialization — S+P+R+N=27 ≠ tot_sov=23): A
- Major 4 (Global search scatter misidentified as profile likelihood): F — contradicts Human Issue #10 (human says "it is nice that the project created several profiles"; Charlie explicitly says these are not profile likelihoods)
- Major 5 (Missing MIF2 convergence trace plots): A
- Major 6 (No particle filter diagnostics — no ESS, no conditional log-likelihood plots): A
- Minor: POMP outperformed by negative binomial regression without structural revision: C
- Minor: IID model AIC is incorrectly computed (2k=2 instead of 2k=4): C
- Minor: Poisson log-likelihood is hardcoded as a literal constant: C
- Minor: No sensitivity analysis for fixed initial conditions: C
- Minor: Probe interpretation is overly optimistic: D — matches Human Issue #8
- Minor: Claim of "well identified" parameters is unsupported: D — matches Human Issue #9
- Minor: Duplicate and misnumbered figure captions: C
- Minor: Typographic errors in equations and references: C

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 1 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "tot_sov is the smoothed spline of S while S is also a dynamic latent state — relationship unexplained")
- Human Issue #4: covered (matched by finding: "observation variable conflates increment ΔZ(t) with accumulating stock N(t) — measurement model dimensionally inconsistent")
- Human Issue #5: covered (matched by finding: "observation variable conflates increment ΔZ(t) with accumulating stock N(t) — measurement model dimensionally inconsistent")
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed

**Findings classification:**
- Finding 1 (mu_IR replaces mu_PR — undisclosed parameter substitution): A — column rename silently patches RDS/code mismatch; human did not raise it
- Finding 2 (N/tot_sov used where R/tot_sov specified): A — code uses N (democracies) instead of R (revolutionary threats) in S→P transition; human did not raise it
- Finding 3 (observation conflates increment and stock; measurement model dimensionally inconsistent): B — ΔZ(t) is a one-year increment but model maps it to accumulating stock N(t); N is absorbing (matches Human Issues #4 and #5)
- Finding 4 (no convergence diagnostics): A — no LL traces, no scatter of final LLs across runs; human did not raise it
- Finding 5 (profile likelihoods are not proper profiles): A — plots are global-search scatter, not re-optimized profiles; human did not raise it
- Finding 6 (aggregate global count not POMP-appropriate): A — treating all countries as one latent chain is a category error; human did not raise it
- Finding 7 (POMP outperformed by 2-parameter NegBin regression): A — lower likelihood than simpler benchmark not adequately addressed; human did not raise it
- Finding 8 (initial conditions implausible and unjustified): A — P=1, R=2, N=1 are arbitrary; no sensitivity analysis; human did not raise it
- Finding 9 (mu_IR/mu_PR completely unidentified): A — parameter ranges 0.035–839 with flat likelihood across 200 runs; human did not raise this parameter specifically
- Finding 10 (figure caption numbering error): C — two figures share "Figure 7" caption; human did not raise it
- Finding 11 (AIC.iid uses only 2 parameters): C — understates IID model's AIC penalty; human did not raise it
- Finding 12 (ρ interpretation as "coding efficiency" non-standard and implausible): C — ρ ≈ 0.07 implies 93% of democratic episodes unrecorded; human did not raise it
- Finding 13 (grammatical and notation inconsistencies throughout): C — transition equation inconsistently uses both N and R in different parts; human did not raise it
- Finding 14 (tot_sov is smoothed spline interpolation of S, not S itself): D — latent S and covariate tot_sov relationship unexplained; S depletes to ~0 while tot_sov grows to ~195 (matches Human Issue #3)
- Finding 15 (no forecast from filtering distribution): C — simulations from t=0, not from filtering distribution; human did not raise it

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "24.01.3 — Conservation-of-population violation: S is never replenished with new sovereign states")
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "24.01.8 — Measurement model excludes democratic reversals by truncating ΔZ(t) at zero")
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: covered (matched by finding: "24.01.1 — Beta is not well identified; profile conclusions are overstated")
- Human Issue #10: covered (matched by finding: "24.01.1 — Beta is not well identified; profile conclusions are overstated")

**Findings classification:**
- 24.01.2: A — Code-math mismatch in S→P transition rate (text uses R(t), code uses N)
- 24.01.3: B — Conservation violation; S is never replenished with newly sovereign states (matches Human Issue #3)
- 24.01.8: B — Measurement model truncates ΔZ(t) at zero, excluding democratic reversals from the likelihood (matches Human Issue #5)
- 24.01.1: B — Beta not well identified; profile likelihood for Beta lacks a clear interior maximum; "well identified" conclusion overstated (matches Human Issues #9 and #10)
- 24.01.9: A — No IF2 convergence trace plots; pair plot of endpoints is not a substitute
- 24.01.4: C — Unclear whether final log-likelihood uses logmeanexp over replicated pfilter runs
- 24.01.5: C — AIC comparability not confirmed; regression and POMP models may not cover identical observations
- M1: C — Effective sample size during particle filtering not reported
- M2: C — Duplicate figure numbering (two "Figure 2" and two "Figure 7")
- M3: C — Typographical error in transition equation (+ instead of =)
- Probes choice: C — Exponential growth rate probe may not be sensitive for sparse annual count data
- rho interpretation: C — Reinterpreting ρ as archival coverage over 200 years needs additional justification

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 2 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 5 | 5 | 8 | 2 |
| B (AI major, human also found) | 3 | 0 | 1 | 3 |
| C (AI minor, human missed) | 5 | 6 | 5 | 7 |
| D (AI minor, human also found) | 2 | 2 | 1 | 0 |
| E (Human found, AI missed) | 5 | 7 | 7 | 6 |
| F (Human-AI contradiction) | 0 | 1 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 3 | 2 | 5 | 5/10 = 50% | 5 | 5 | 10/15 = 67% |
| Charlie | 0 | 2 | 7 | 2/9 = 22% | 5 | 6 | 11/13 = 85% |
| Doug | 1 | 1 | 7 | 3/10 = 30% | 8 | 5 | 13/15 = 87% |
| Evan | 3 | 0 | 6 | 4/10 = 40% | 2 | 7 | 9/12 = 75% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #1: The dataset must somehow determine whether an election is free and fair, since many autocracies claim to have a democratic mandate. A brief explanation would help the reader. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #6: The $P$ and $R$ components are not clearly defined. $P$ should maybe be defined as the change in the number of states that are still under the control of powerful elites who are for the current state. Then the states that are under heavy influence of the elites would then transition to state $R$, which is the change in the number of states that enter a revolution, or revolution is threatened. The way the model is defined leaves me to believe that there should be a state after $N$, which would be the final compartment for states that achieve democracy, instead of remaining in negotiations, or going back to revolution. The variables $\beta$ and $R(t)$ are introduced, and while $R(t)$ is previously defined, $\beta$ isn't given a definition, so at this point, no intuition is given as to what this variable represents. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #7: In Fig. 4, $\beta$ and $\mu_{PR}$ plots would be clearer with the x-axis on a log scale. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 3 out of 10 human issues (30%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #2: Is there an error in Fig. 1? $Z(t)$ seems to be defined as non-negative. It is unusual to require $\Delta(Z(t))$ to be non-negative. (Covered only by Alex)
- Human Issue #4: $\Delta Z(t)$ is described as the number of democracies, but is it actually the change in that number? Perhaps the plot of the graphs for $Z(t)$ and $\Delta Z(t)$ seem incorrectly labeled. The graph on the right looks like the differences of the $Z(t)$ values, without performing the transform defined for $\Delta Z(t)$, while the graph on the left aligns more with the newly defined $\Delta Z(t)$, the positive change of new democratic states. (Covered only by Doug)
- Human Issue #10: In the profile, $k$ is not identifiable as it has values across its whole range that maximize the likelihood. It is nice that the project created several profiles of different parameters. (Covered only by Evan)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 1 |
| Charlie | 0 |
| Doug | 1 |
| Evan | 1 |
