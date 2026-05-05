# Ned-Clean Analysis — W21 Project 06

---

## Human Issues

1. Motivation was somewhat unclear: explain the relationship between studying volatility and understanding the GameStop story.
2. All the models used are stationary, and the WallStreetBets intervention is perhaps temporary — there might be room for improvement on these business-as-usual financial models (e.g., volatility might increase with increasing stock price during deliberate manipulation, opposite of the usual pattern).
3. Make sure the text explains what is going on: usually, we only show code and computer output that is part of the story explained in the text.
4. In Conclusions: compare the maximized log likelihood, not the median log likelihood from a stochastic search.
5. If some parameters are weakly identified, that is not necessarily a problem for the model: it just means that those parts of the model are not so important.
6. The maximized likelihood may be more relevant than the median when doing multiple searches to numerically maximize the likelihood.
7. The assumptions and purposes of the different models could be discussed more, to put the maximized likelihoods and other results in context.
8. In the global search, the convergence points form two clusters, most clearly seen in log likelihood vs mu_h.
9. Show returns with a mean, and don't also show demeaned returns which is visually almost identical.
10. Some sections are short on motivation: if you have a section on filtering simulated data, you should explain briefly why it is there, and what you learn from it.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding #13 — anomalous short-squeeze event not given special modeling treatment)
- Human Issue #3: covered (matched by finding #8 — simulation comparison plot text does not match the code, same class of concern: code/output not integrated into narrative)
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: covered (matched by finding #11 — pairs plots not discussed; notes multi-modality including mu_h clusters)
- Human Issue #9: missed
- Human Issue #10: missed

**Findings classification:**
- Finding 1 (near-verbatim replication of course slides, MAJOR): A — no human equivalent
- Finding 2 (global search box does not cover local search optimum, MAJOR): A — no human equivalent
- Finding 3 (AIC comparison across ARMA/GARCH/POMP invalid, MAJOR): A — no human equivalent
- Finding 4 (non-convergence ignored, MAJOR): A — no human equivalent
- Finding 5 (Monte Carlo error in log-likelihood not acknowledged, MAJOR): A — no human equivalent
- Finding 6 (ARMA residual ACF not investigated, MAJOR): A — no human equivalent
- Finding 7 (GARCH(4,2) selection unjustified; AIC dismissal incorrect, MAJOR): A — no human equivalent
- Finding 8 (simulation plot text appears after the code it describes, MINOR): D — matches Human Issue #3
- Finding 9 (covariate alignment for GME_rproc.filt not verified, MINOR): C — no human equivalent
- Finding 10 (no likelihood ratio test for nested leverage models, MINOR): C — no human equivalent
- Finding 11 (pairs plots shown but not discussed; multi-modality visible, MINOR): D — matches Human Issue #8
- Finding 12 (ARMA(1,3) not the global AIC minimum; neighborhood criterion subjective, MINOR): C — no human equivalent
- Finding 13 (short-squeeze event not given special model treatment, MINOR): D — matches Human Issue #2
- Finding 14 (conclusion internally inconsistent: -260.88 vs -262.88 AIC discrepancy, MINOR): C — no human equivalent (different from max-vs-median concern)
- Finding 15 (heavy reliance on past student projects not clearly disclosed, MINOR): C — no human equivalent

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 3 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

Human Recall = (0+3) / (0+3+7) = 3/10 = **30%**
AI-Unique Rate = (7+5) / (7+0+5+3) = 12/15 = **80%**

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding #13 — AIC for POMP uses median log-likelihood)
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding #13 — same finding also covers H4; max-vs-median concern)
- Human Issue #7: missed
- Human Issue #8: covered (matched by finding #12 — pairs plots not interpreted; notes multi-modality and mu_h spread)
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding #10 — initial simulation does not match data and this discrepancy is insufficiently explained)

**Findings classification:**
- Finding 1 (AIC comparison invalid across ARMA/GARCH/POMP, MAJOR): A — no human equivalent (human asks for more context, not technical invalidity)
- Finding 2 (profile likelihoods absent, MAJOR): A — no human equivalent
- Finding 3 (non-convergence acknowledged but not remediated, MAJOR): A — no human equivalent
- Finding 4 (global search starts from if1[[1]], MAJOR): A — no human equivalent
- Finding 5 (insufficient particle count Np=2000, MAJOR): A — no human equivalent
- Finding 6 (GARCH AIC uses tseries non-standard log-likelihood, MAJOR): A — no human equivalent
- Finding 7 (no non-mechanistic benchmark at correct level, MINOR): C — no human equivalent
- Finding 8 (ARMA model selection lacks convergence check, MINOR): C — no human equivalent
- Finding 9 (simulation-based diagnostics absent, MINOR): C — no human equivalent
- Finding 10 (initial simulation deviates substantially from data; no post-fit simulation shown, MINOR): D — matches Human Issue #10
- Finding 11 (ARMA residual ACF: volatility clustering explanation missing, MINOR): C — no human equivalent
- Finding 12 (pairs plots produced but not interpreted; multi-modality visible, MINOR): D — matches Human Issue #8
- Finding 13 (AIC for POMP computed from median, not maximum, log-likelihood, MINOR): D — matches Human Issues #4 and #6 (one finding, two human issues covered)
- Finding 14 (tanh(G) leverage code not explained in text, MINOR): C — no human equivalent
- Finding 15 (ARMA(1,3) equation missing epsilon_{n-3} term, MINOR): C — no human equivalent

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 3 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

Note: D=3 AI findings cover 4 human issues (finding #13 covers both H4 and H6). Human Recall denominator uses human-issue counts: B_h=0, D_h=4, E=6.

Human Recall = (0+4) / (0+4+6) = 4/10 = **40%**
AI-Unique Rate = (6+6) / (6+0+6+3) = 12/15 = **80%**

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding #15 — no discussion of model limitations for unprecedented price spike)
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding #9 — AIC calculation uses median log-likelihood)
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding #9 — same finding; max vs median concern)
- Human Issue #7: covered (matched by finding #4 — invalid cross-model log-likelihood comparison; both concern inadequacy of the model comparison)
- Human Issue #8: covered (matched by finding #12 — global search box for mu_h inconsistently narrow; addresses same mu_h parameter behavior)
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding #1 — simulated-data particle filter presented without clear benchmark qualification)

**Findings classification:**
- Finding 1 (simulated-data particle filter presented without benchmark qualification, MAJOR): B — matches Human Issue #10
- Finding 2 (global IF2 search initialized from previous mif2 result, MAJOR): A — no human equivalent
- Finding 3 (no benchmark comparison against non-mechanistic model, MAJOR): A — no human equivalent
- Finding 4 (invalid cross-model log-likelihood comparison, MAJOR): B — matches Human Issue #7
- Finding 5 (no profile likelihoods for key parameters, MAJOR): A — no human equivalent
- Finding 6 (non-convergence acknowledged but not remediated, MAJOR): A — no human equivalent
- Finding 7 (quantitative model adequacy assessment incomplete, MAJOR): A — no human equivalent
- Finding 8 (pairs plot cutoff inconsistent between local and global searches, MINOR): C — no human equivalent (different from H8's two-clusters concern)
- Finding 9 (AIC uses median log-likelihood, MINOR): D — matches Human Issues #4 and #6
- Finding 10 (conclusion conflates optimization convergence with goodness of fit, MINOR): C — no human equivalent
- Finding 11 (rw.sd values unjustified, MINOR): C — no human equivalent
- Finding 12 (global search box for mu_h does not include local search optimum, MINOR): D — matches Human Issue #8
- Finding 13 (stationarity not formally tested, MINOR): C — no human equivalent
- Finding 14 (model equation notation error using Y_n in rproc, MINOR): C — no human equivalent
- Finding 15 (no discussion of model limitations for extreme price spike, MINOR): D — matches Human Issue #2

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 3 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

Note: D=3 AI findings cover 4 human issues (finding #9 covers both H4 and H6). Human Recall denominator: B_h=2, D_h=4, E=4.

Human Recall = (2+4) / (2+4+4) = 6/10 = **60%**
AI-Unique Rate = (5+5) / (5+2+5+3) = 10/15 = **66.7%**

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by Gaussian measurement model finding — Gaussian model inappropriate for GME heavy-tailed returns; same concern as inadequacy of standard model for extreme event)
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding 21.06.3 — phi and sigma_eta identifiability; notes this is weak identifiability not optimizer failure, aligning with human's view that weak ID is not necessarily a problem)
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding 21.06.1 — AIC cross-class comparison needs qualification; both concern contextualizing the model comparison)
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding 21.06.13 — filtering-on-simulated-data section lacks clarity about what the log-likelihood represents)

**Findings classification:**
- 21.06.5 (MLE parameter estimates not reported, MAJOR): A — no human equivalent
- 21.06.14 (no profile likelihoods or confidence intervals, MAJOR): A — no human equivalent
- 21.06.4 (fixed leverage model not compared to stochastic leverage, MAJOR): A — no human equivalent
- 21.06.2 (GARCH AIC table shows numerical instability, MAJOR): A — no human equivalent
- 21.06.1 (AIC cross-class comparison needs qualification, MINOR): D — matches Human Issue #7
- 21.06.3 (phi and sigma_eta identifiability; weak ID not optimizer failure, MINOR): D — matches Human Issue #5
- 21.06.12 (ARMA residual ACF significant correlations, MINOR): C — no human equivalent
- 21.06.13 (filtering-on-simulated-data section not clearly explained, MINOR): D — matches Human Issue #10
- ESS not monitored (MINOR): C — no human equivalent
- Gaussian measurement model inappropriate for heavy tails (MINOR): D — matches Human Issue #2
- Typographical errors (MINOR): C — no human equivalent

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 3 |
| D (AI minor, human also found) | 4 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

Human Recall = (0+4) / (0+4+6) = 4/10 = **40%**
AI-Unique Rate = (4+3) / (4+0+3+4) = 7/11 = **63.6%**

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 7 | 6 | 5 | 4 |
| B (AI major, human also found) | 0 | 0 | 2 | 0 |
| C (AI minor, human missed) | 5 | 6 | 5 | 3 |
| D (AI minor, human also found) | 3 | 3 | 3 | 4 |
| E (Human found, AI missed) | 7 | 6 | 4 | 6 |

Note: For Human Recall, D counts human issues covered by AI minor findings (may exceed AI finding count D when one AI finding covers two human issues). For AI-Unique Rate, D counts AI findings categorized as D.

---

## Per-Reviewer Metrics

| Reviewer | Human Recall | AI-Unique Rate |
|----------|-------------:|---------------:|
| Alex | 30% (3/10) | 80% (12/15) |
| Charlie | 40% (4/10) | 80% (12/15) |
| Doug | 60% (6/10) | 66.7% (10/15) |
| Evan | 40% (4/10) | 63.6% (7/11) |

Human Recall = (B_h + D_h) / (B_h + D_h + E), where B_h and D_h count human issues covered.
AI-Unique Rate = (A + C) / (A + B_f + C + D_f), where B_f and D_f count AI findings matched to human issues.

---

## Cross-Reviewer Aggregation

### Consensus Misses

Human issues missed by every reviewer:

- **Human Issue #1** (unclear motivation for studying volatility in the GameStop context): missed by Alex, Charlie, Doug, Evan.
- **Human Issue #9** (show returns with a mean; do not also show demeaned returns that look visually identical): missed by Alex, Charlie, Doug, Evan.

Count: 2 out of 10 human issues (20%).

### Unique Finds Per Reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Alex uniquely covers **Human Issue #3** (text should explain what is going on; code/output only shown as part of the narrative). No other reviewer addresses this.
- Evan uniquely covers **Human Issue #5** (weakly identified parameters are not necessarily a problem — they just mean those model aspects are less important). No other reviewer makes this point; others treat non-convergence purely as a problem to fix.

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 1 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 1 |

### Universal AI-Only Flags

Issues raised as AI-only (A or C) by every reviewer that the human did not mention:

No single concern appears in all four AI reviews as a finding absent from the human review. The closest near-universal flags (raised by three of four reviewers as AI-unique) are:

- Profile likelihoods absent: Charlie (A), Doug (A), Evan (A) — Alex does not have a standalone profile likelihood finding.
- Non-convergence not remediated: Alex (A), Charlie (A), Doug (A) — Evan's treatment of convergence is categorized D (matched to Human #5).
- Invalid AIC cross-model comparison (technical invalidity): Alex (A), Charlie (A) — Doug's equivalent finding is B (matched to Human #7), Evan's is D (matched to Human #7).

Universal AI-only flags (all four): **0**.
