# Figure 4 Case Studies — Rows Not Spelled Out in the Paper

The final appendix in `main.tex` gives full write-ups to only a handful of Figure 4's rows (chosen for the 3-page budget), plus a couple of examples that sit outside Figure 4 entirely. This file archives the remaining rows in full — specific examples kept here for completeness and verifiability, rather than in the paper itself.

Each entry below is copied verbatim from `proposal/ms.qmd`'s Appendix A as of 2026-09-29, including links.

**Which rows made it into the actual paper, and why:**
- **Row 1** (this project, W21 Project 14) **is** in the paper — but not as a validated finding. Its technical premise was checked and found to be **false**: the claim that the global search "inherits an already-cooled tuning state" from `mif2(mifs_local[[1]], params=...)` does not hold up against `pomp`'s actual `mif2` method dispatch (confirmed by reading the S4 method chain and by empirical testing in R — a control run with a genuinely frozen `rw.sd` was clearly distinguishable from the actual code's behavior, which moved substantially across iterations like a normal, working search). All four AI agents converged on this same incorrect claim independently — Doug via a persisted MetaSkill skill file (`pomp-global-search-init-audit`) that flags this pattern "regardless" of verification, and Alex/Charlie/Evan via an apparently shared but unverified inference about R/pomp object-reuse semantics. Several reviews additionally cite "Wheeler et al. (2024)" for this claim; the actual paper text contains no such discussion. The paper uses this as a deliberate counter-example, paired with the genuine W22 Project 10 `dmeasure`/`rmeasure` bug: agreement across all four agents is not, by itself, evidence of correctness.
- **Row 5** (immigration-model bug, W25 Project 5) and **Row 11** (φ duplicate-name bug, W21 Project 16) are both in the paper in full, as the Baseline-unique and Orchestrator-unique representative examples.
- Rows 2, 3, 4, 6, 8, 9, 10, and 12 are **not** written up in the paper — they're archived below only.

---

## Row 1. Global search inherits cooled schedule, not truly global (optimization flaw) (2021, Project 14)

**Status: technical premise debunked — see note above. Included in the paper as a counter-example, not as a validated finding.**

* [Project](https://ionides.github.io/531w21/final_project/project14/blinded.html)
* [Human review](https://ionides.github.io/531w21/final_project/project14/comments.html)
* [Baseline, Alex](https://github.com/ionides/jagged-ai-peer-review/blob/main/results/alex/alex-review-W21_PROJECT14.md)
* [CourseGuided, Charlie](https://github.com/ionides/jagged-ai-peer-review/blob/main/results/charlie/charlie-review-W21_PROJECT14.md)
* [MetaSkill, Doug](https://github.com/ionides/jagged-ai-peer-review/blob/main/results/doug/doug-review-W21_PROJECT14.md)
* [Orchestrator, Evan](https://github.com/ionides/jagged-ai-peer-review/blob/main/results/evan/evan-review-W21_PROJECT14.md)
* [Comparator](https://github.com/ionides/jagged-ai-peer-review/blob/main/results/comparator/comparator-W21_PROJECT14.md)

Standard practice for maximizing the likelihood of a POMP model by iterated filtering (IF2) is to run many independent search chains from dispersed starting points, each following its own perturbation schedule that cools from a wide initial spread down to a narrow one over many iterations. In this project, each global-search replicate was instead initialized by calling `mif2(mifs_local[[1]], params = ...)`, so every global chain inherited the tuning state that is already cooled, ie. the random-walk standard deviations, cooling schedule, and number of filtering iterations are already completed from the first local-search chain when a perturbation schedule should have started fresh from a broad initial spread. All four review agents identified this same bug. As the Orchestrator put it, "this substantially reduces the exploration capacity of the global phase". The tuning parameters were already cooled from the local search, limiting searching the parameter space, which undermines the paper's claim to have performed a genuine global optimization.

---

## Row 2. Cross-family log-likelihood comparison invalid (scale mismatch) (2021, Project 13)

* [Project](https://ionides.github.io/531w21/final_project/project13/blinded.html)
* [Human review](https://ionides.github.io/531w21/final_project/project13/comments.html)
* [Baseline, Alex](https://github.com/ionides/jagged-ai-peer-review/blob/main/results/alex/alex-review-W21_PROJECT13.md)
* [CourseGuided, Charlie](https://github.com/ionides/jagged-ai-peer-review/blob/main/results/charlie/charlie-review-W21_PROJECT13.md)
* [MetaSkill, Doug](https://github.com/ionides/jagged-ai-peer-review/blob/main/results/doug/doug-review-W21_PROJECT13.md)
* [Orchestrator, Evan](https://github.com/ionides/jagged-ai-peer-review/blob/main/results/evan/evan-review-W21_PROJECT13.md)
* [Comparator](https://github.com/ionides/jagged-ai-peer-review/blob/main/results/comparator/comparator-W21_PROJECT13.md)

It is good data-analysis practice to check a complex nonlinear POMP model against a simple non-mechanistic benchmark, such as ARIMA, by comparing log-likelihoods: a POMP model that fits appreciably worse than a simple alternative calls its added complexity into question. Log-likelihoods are comparable across model classes only if the models are fit to the same representation of the data under comparable observation models, and only after some allowance is made for the models' differing complexity, for instance via AIC. This project compares an ARIMA log-likelihood of $-4091$ against a POMP log-likelihood of $-3791$ and concludes the POMP model fits better, but violates both conditions: the ARIMA model was fit to the first-differenced case counts under a Gaussian innovations model, while the POMP model was fit to the full undifferenced daily case counts under a different, count-based observation model, so the two log-likelihoods are not on a comparable scale; and the ARIMA model has only 7 parameters against the POMP model's 16, so even a valid comparison would need to be penalized for this disparity in complexity rather than made on raw log-likelihood alone. All four agents identified the data-representation problem, and Doug additionally flagged the parameter-count issue: "even if the observation models were comparable, AIC or a penalized criterion must be used rather than raw log-likelihood." As Charlie put it, the appropriate fix for the first issue is to "either fit both models to the same untransformed data with the same observation model, or explicitly acknowledge the incomparability and refrain from using the likelihood difference as evidence for POMP superiority." Neither issue was raised in any of the five human review points for this project.

---

## Row 3. No ESS or particle filter diagnostics reported (verification gap) (2021, Project 15)

* [Project](https://ionides.github.io/531w21/final_project/project15/blinded.html)
* [Human review](https://ionides.github.io/531w21/final_project/project15/comments.html)
* [Baseline, Alex](https://github.com/ionides/jagged-ai-peer-review/blob/main/results/alex/alex-review-W21_PROJECT15.md)
* [CourseGuided, Charlie](https://github.com/ionides/jagged-ai-peer-review/blob/main/results/charlie/charlie-review-W21_PROJECT15.md)
* [MetaSkill, Doug](https://github.com/ionides/jagged-ai-peer-review/blob/main/results/doug/doug-review-W21_PROJECT15.md)
* [Orchestrator, Evan](https://github.com/ionides/jagged-ai-peer-review/blob/main/results/evan/evan-review-W21_PROJECT15.md)
* [Comparator](https://github.com/ionides/jagged-ai-peer-review/blob/main/results/comparator/comparator-W21_PROJECT15.md)

A particle filter's log-likelihood estimate is only as trustworthy as the health of the filter itself: if the effective sample size (ESS) of the particle population collapses at some point in the time series, a small number of particles end up carrying nearly all the weight, and the resulting estimate can become highly variable or biased without any visible sign in the final reported number. Standard practice is therefore to monitor ESS, together with complementary diagnostics such as conditional log-likelihoods per time step, so that a reader can distinguish a model that genuinely fits the data poorly from a particle filter that silently degenerated. This project presented no such diagnostics, relying only on visual comparisons of unconditional forward simulations against the observed data. All four agents flagged this gap independently. Alex noted that "the project does not present any particle filter diagnostics such as effective sample size (ESS) over time, which could indicate degeneracy in the filter," and that with 1,000 particles across a 306-day series, "filter collapse is a real concern." Charlie and Doug both observed that the diagnostic assessment relied entirely on unconditional forward simulation, with "no conditional log-likelihoods per time step... no effective sample size (ESS) monitoring... no filtering distribution plots." Evan reached the same conclusion, noting that "effective sample size from the particle filter is not monitored," a concern heightened by the "early epidemic dynamics that may produce degenerate filtering distributions." Without any of these diagnostics, a reader has no way to know whether the reported log-likelihoods reflect the model's genuine fit to the data or an undetected filtering failure. None of these four review points was raised in either of the two human review points for this project.

---

## Row 4. Modifying one variable silently changes another (implementation bug) (2024, Project 12; 2025, Project 15)

*Project 12:*
* [Project](https://ionides.github.io/531w24/final_project/project12/blinded.html)
* [Human review](https://ionides.github.io/531w24/final_project/project12/comments.html)
* [Baseline, Alex](https://github.com/ionides/jagged-ai-peer-review/blob/main/results/alex/alex-review-W24_PROJECT12.md)
* [Comparator](https://github.com/ionides/jagged-ai-peer-review/blob/main/results/comparator/comparator-W24_PROJECT12.md)

*Project 15:*
* [Project](https://ionides.github.io/531w25/final_project/project15/blinded.html)
* [Human review](https://ionides.github.io/531w25/final_project/project15/comments.html)
* [Baseline, Alex](https://github.com/ionides/jagged-ai-peer-review/blob/main/results/alex/alex-review-W25_PROJECT15.md)
* [Comparator](https://github.com/ionides/jagged-ai-peer-review/blob/main/results/comparator/comparator-W25_PROJECT15.md)

The reliability of a computational pipeline depends on each step actually operating on the data its author intends; when a variable or output file is reused for two different purposes, the second write can silently destroy the first result, and because the code still runs without error and produces plausible-looking numbers, nothing in the rendered output signals that anything went wrong. In the first project, the code does exactly this to itself: `global_results <- global_results %>% arrange(-loglik) %>% head(...)` replaces the full set of global-search results with only its top six rows before the profile-likelihood step runs, so any downstream analysis that assumes access to the full search is silently working from a truncated dataset. In the second, unrelated project, two separate global searches, one under a normal-distribution stochastic-volatility model and one under a $t$-distribution variant, both write their output to the same file, `btc_global_params.csv`, via `write.csv`, which overwrites by default; when the document renders both chunks in sequence, the first search's results are silently destroyed by the second before they can be used. Both instances were caught only by the agent that read the code closely enough to trace variable and file reuse across chunks.

---

## Row 5. Code does not implement the model as written (implementation bug) (2025, Project 5)

* [Project](https://ionides.github.io/531w25/final_project/project05/blinded.html)
* [Human review](https://ionides.github.io/531w25/final_project/project05/comments.html)
* [Baseline, Alex](https://github.com/ionides/jagged-ai-peer-review/blob/main/results/alex/alex-review-W25_PROJECT05.md)
* [Comparator](https://github.com/ionides/jagged-ai-peer-review/blob/main/results/comparator/comparator-W25_PROJECT05.md)

A `pomp` object's process model is compiled once from its C snippet when the object is constructed; changing the object's parameter values afterward, for instance via `coef(...) <- c(...)`, updates what values will be plugged into that compiled model, but it does not recompile the model itself. If the intended change is to the model's structure, such as adding a new dynamic like immigration, and not just its parameter values, a fresh `pomp(...)` call rebuilding the object is required, or the change silently never takes effect. This project's code in chunk `setup-immi` updates the R objects `paramnames` and `rproc` in memory and sets new coefficients on `seir_spline_model` via `coef(seir_spline_model) <- c(...)`, but never makes a second `pomp(...)` call to rebuild the model with the new `rproc` (containing `immigration_rate`) and updated `paramnames`. As a result, the "POMP Model with Immigration" local and global searches almost certainly ran using the original process model without immigration dynamics, invalidating the entire comparison between the two POMP models. This is the most serious technical error in the project. This AI review comment is supported by subsequent human investigation of the code, specifically by inspection of lines 425 and 565 of `blinded.Rmd`. In this case, the AI agent least burdened by additional instructions saw deepest into the details of the code. This is consistent with the statistical observation that providing domain-specific skill files can confer little or no advantage.

---

## Row 6. Computation produces wrong values without error (implementation bug) (2024, Project 2)

* [Project](https://ionides.github.io/531w24/final_project/project02/blinded.html)
* [Human review](https://ionides.github.io/531w24/final_project/project02/comments.html)
* [Baseline, Alex](https://github.com/ionides/jagged-ai-peer-review/blob/main/results/alex/alex-review-W24_PROJECT02.md)
* [Comparator](https://github.com/ionides/jagged-ai-peer-review/blob/main/results/comparator/comparator-W24_PROJECT02.md)

Like many R constructor functions, `pomp()` does not raise an error when it receives an argument name it does not recognize; it simply ignores it. This means a simple misspelling of an argument, invisible to a cursory read of the code, can silently fail to configure the model as intended, with no diagnostic message to reveal the mistake. In this project, the variable `logCPUE` is removed from the `pomp` object during model setup, and the `obs_names` argument passed to `pomp()` is not a valid argument name (the correct name is `obsnames`), so it is silently ignored rather than raising an error. Because `pomp`'s constructor does not flag this unrecognized argument, the project's specification of which variable to treat as the observed data silently fails, and the model proceeds to fit against a different observation than intended. As with the previous item, this is a case where the code executes without any visible error and produces a complete, plausible-looking analysis, while actually computing something other than what was intended.

---

## Row 7. Confidence interval procedure is wrong (methodology flaw) (2024, Project 16)

* [Project](https://ionides.github.io/531w24/final_project/project16/blinded.html)
* [Human review](https://ionides.github.io/531w24/final_project/project16/comments.html)
* [CourseGuided, Charlie](https://github.com/ionides/jagged-ai-peer-review/blob/main/results/charlie/charlie-review-W24_PROJECT16.md)
* [MetaSkill, Doug](https://github.com/ionides/jagged-ai-peer-review/blob/main/results/doug/doug-review-W24_PROJECT16.md)
* [Comparator](https://github.com/ionides/jagged-ai-peer-review/blob/main/results/comparator/comparator-W24_PROJECT16.md)

A valid profile likelihood for a parameter requires, at each grid value of that parameter, holding it fixed and re-optimizing the likelihood over every other parameter; only a curve constructed this way supports a valid likelihood-ratio-based confidence interval. Taking a subset or envelope of an already-completed, unconstrained global search is a fundamentally different procedure, even though the resulting plot can look superficially similar. CourseGuided and MetaSkill both recognized that this project's "profile likelihood" plots are not true profile likelihoods in this sense: the underlying code constructs them by filtering the global-search results, `profile_results %>% filter(loglik > max(loglik) - 15) %>% group_by(round(Beta_v, 2.0)) %>% filter(rank(-loglik) < 3)`, which takes the upper envelope of a global search binned by rounded parameter value, rather than fixing each target parameter at a grid of values and re-optimizing over the remaining parameters at each point. As CourseGuided noted, the global search may not have representative coverage at every parameter value, so this envelope approach "can underestimate the true profile" and produce confidence intervals that are never actually reported numerically. MetaSkill reached the same diagnosis independently, describing the plots as "misidentified global-search scatter plots rather than true profile likelihoods." Neither the Baseline agent nor the human reviewer raised this distinction, which requires familiarity with how a profile likelihood is properly constructed, exactly the kind of course-specific methodological knowledge the skill files were designed to supply.

---

## Row 8. No simpler baseline model for comparison (model evaluation) (2022, Project 11)

* [Project](https://ionides.github.io/531w22/final_project/project11/blinded.html)
* [Human review](https://ionides.github.io/531w22/final_project/project11/comments.html)
* [CourseGuided, Charlie](https://github.com/ionides/jagged-ai-peer-review/blob/main/results/charlie/charlie-review-W22_PROJECT11.md)
* [MetaSkill, Doug](https://github.com/ionides/jagged-ai-peer-review/blob/main/results/doug/doug-review-W22_PROJECT11.md)
* [Comparator](https://github.com/ionides/jagged-ai-peer-review/blob/main/results/comparator/comparator-W22_PROJECT11.md)

Checking a complex mechanistic model's log-likelihood against a simple non-mechanistic benchmark is a standard way to tell whether the added complexity is earning its keep (see Row 2's discussion of this same principle). Both CourseGuided and MetaSkill noted, in near-identical terms, that no such benchmark, an ARMA fit or an IID negative-binomial model, for instance, was compared against the POMP model in this project. Without one, there is no way to tell whether the mechanistic model's fit represents a meaningful improvement over a much simpler statistical description of the same data, a comparison the course materials treat as a standard, near-mandatory check.

---

## Row 9. Too few starting values explored in fitting (optimization flaw) (2025, Project 3)

* [Project](https://ionides.github.io/531w25/final_project/project03/blinded.html)
* [Human review](https://ionides.github.io/531w25/final_project/project03/comments.html)
* [CourseGuided, Charlie](https://github.com/ionides/jagged-ai-peer-review/blob/main/results/charlie/charlie-review-W25_PROJECT03.md)
* [MetaSkill, Doug](https://github.com/ionides/jagged-ai-peer-review/blob/main/results/doug/doug-review-W25_PROJECT03.md)
* [Comparator](https://github.com/ionides/jagged-ai-peer-review/blob/main/results/comparator/comparator-W25_PROJECT03.md)

A global search is only as good as its coverage of the parameter space: it needs enough dispersed starting points to have a realistic chance of locating the global optimum rather than reporting back a local one, and this requirement only grows more demanding as the number of free parameters increases. CourseGuided noted that the global search for this 13-parameter model sampled only 10 random starting points, well below the course-recommended standard of 20 starting points at run_level 2 or 100 at run_level 3: "with only 10 starts in a high-dimensional space, the search may miss the global maximum." MetaSkill reached the same conclusion independently, noting that "global search uses only 10 replicates with Nmif=50, insufficient to confirm convergence." In a parameter space with this many dimensions, a handful of starting points is unlikely to adequately cover the space, so a search finding a consistent optimum from so few starts is at best weak evidence, and at worst is simply reporting the same local optimum every time.

---

## Row 10. Incorrect biological formula in model (domain error) (2021, Project 11)

* [Project](https://ionides.github.io/531w21/final_project/project11/blinded.html)
* [Human review](https://ionides.github.io/531w21/final_project/project11/comments.html)
* [Orchestrator, Evan](https://github.com/ionides/jagged-ai-peer-review/blob/main/results/evan/evan-review-W21_PROJECT11.md)
* [Comparator](https://github.com/ionides/jagged-ai-peer-review/blob/main/results/comparator/comparator-W21_PROJECT11.md)

A compartmental epidemic model's initial conditions are only biologically valid if they respect the model's own closed-population assumption: the compartments at time zero must sum to the total population $N$, since every individual has to be in exactly one compartment. The Orchestrator identified that this project's initial conditions violate that constraint: with $S \approx 8.4$ million, $E = 90{,}000$, $I = 66{,}000$, and $R \approx 1.6$ million, the compartments sum to $N + 156{,}000$, about 156,000 more individuals than the population actually contains. Checking this required verifying that a set of initial-condition formulas is internally consistent with the model's own stated population size, a basic conservation-law check rather than a code-syntax or methodology issue, and one the other three agents and the human reviewer all missed.

---

## Row 11. Profile too flat/noisy to extract CIs (identifiability issue) (2021, Project 16)

* [Project](https://ionides.github.io/531w21/final_project/project16/blinded.html)
* [Human review](https://ionides.github.io/531w21/final_project/project16/comments.html)
* [Orchestrator, Evan](https://github.com/ionides/jagged-ai-peer-review/blob/main/results/evan/evan-review-W21_PROJECT16.md)
* [Comparator](https://github.com/ionides/jagged-ai-peer-review/blob/main/results/comparator/comparator-W21_PROJECT16.md)

A profile likelihood is only informative about a parameter's identifiability if that parameter is genuinely held fixed while every other parameter is re-optimized (see Row 7's discussion of this same requirement); if an implementation bug lets the "fixed" parameter silently vary instead, the resulting curve reflects the bug rather than the model, and could easily be mistaken for a genuine scientific finding about the data. The Orchestrator identified exactly this kind of bug in the profile likelihood for the parameter $\phi$ in this project: the code constructs the starting values for the profile as `c(unlist(guesses[i,]), params_test)`, which concatenates two named vectors that both contain an entry named `phi`; R's behavior when a vector has duplicate names is to use the first occurrence, so the profiled value of $\phi$ may silently be overridden by whichever value appears first in `guesses`. Compounding this, only `nprof=2` starting points are used per profiled value of $\phi$, which the Orchestrator noted is "far too sparse to reliably evaluate the profile" even if the fixing were implemented correctly. Together, these two issues would produce a profile likelihood curve that looks flat or noisy for reasons that have nothing to do with the parameter's actual identifiability.

---

## Row 12. Results lack parameter estimates or captions (omission) (2022, Project 19)

* [Project](https://ionides.github.io/531w22/final_project/project19/blinded.html)
* [Human review](https://ionides.github.io/531w22/final_project/project19/comments.html)
* [Orchestrator, Evan](https://github.com/ionides/jagged-ai-peer-review/blob/main/results/evan/evan-review-W22_PROJECT19.md)
* [Comparator](https://github.com/ionides/jagged-ai-peer-review/blob/main/results/comparator/comparator-W22_PROJECT19.md)

A figure in a data-analysis report is only useful to a reader if its caption identifies what is being shown -- which model produced it, what quantity is plotted, how to read its axes -- since without this a reader cannot verify the underlying analysis from the figure alone and must reconstruct the missing context by re-reading the source code. The Orchestrator noted that none of this project's figures have descriptive captions, writing that this makes "the manuscript difficult to navigate without closely following the code chunks." While each individual missing caption is a minor issue, the cumulative effect leaves a reader unable to determine, from the figures alone, which model or search procedure produced any given plot, an omission serious enough in aggregate to hinder verification of the project's own reported results.
