# Final AI Review: STATS 531 W21 Final Project 05

---

## Overall Assessment

This project tackles a well-motivated scientific question — whether POMP models can capture the sharp reduction in influenza A contact rate associated with COVID-19 social distancing in the 2019–20 season in Michigan. The framing is clear, the data are appropriate, and the use of pomp infrastructure (mif2, replicated pfilter, logmeanexp) is mechanically correct. However, the analysis stops well short of answering its own research question. Three POMP models are fit using local search only from single starting points, no non-mechanistic benchmark is provided, no profile likelihoods or confidence intervals are computed, and the third model — the one designed to capture contact rate reduction — hard-codes the magnitude of the reduction rather than estimating it. The analysis is concluded prematurely on the grounds that all three models are inadequate, but the inadequacy diagnosis is itself unreliable without a global search. The paper demonstrates engagement with the course tools but does not reach a stage where scientific conclusions can be drawn.

---

## Key Strengths

**ID: 21.05.S1**
The research question is scientifically coherent and well-motivated. Linking COVID-19 behavioral change to a decline in influenza contact rate is a plausible and testable hypothesis. The choice of the 2019–20 season is appropriate as it contains both pre- and post-behavioral-change data within a single season.

**ID: 21.05.S2**
The pomp computational infrastructure is used correctly in key respects. Log-likelihoods are aggregated via `logmeanexp` applied to replicated pfilter runs (10 replicates, Np=20000 for evaluation), and mif2 is applied with parameter transformations (log for positive-constrained parameters, logit for probabilities). These are appropriate practices.

**ID: 21.05.S3**
Iterating across three model variants (SIR, SEIR, time-varying SIR) shows systematic model-building effort and gives the reader some basis for comparing structures.

---

## Major Points

**ID: 21.05.M1**
**Concern:** No non-mechanistic benchmark comparison.
**Why it matters:** Without an ARMA, auto-regressive negative-binomial, or other non-mechanistic baseline, the POMP log-likelihoods (-1278 for SIR, -861 for SEIR after local search) cannot be evaluated. A POMP model that loses to ARMA is informative; one that outperforms it is compelling. Currently the absolute log-likelihood values are uninterpretable.
**Severity:** Major
**Suggested author action:** Fit an ARMA(p,q) or auto-regressive negative-binomial model to the same 52-week series and report its log-likelihood alongside the POMP models.

**ID: 21.05.M2**
**Concern:** No global search; convergence is not demonstrated.
**Why it matters:** All three mif2 runs start from a single named parameter vector. The trace plots (Figures 7, 9, 12) show parameters and log-likelihood bouncing in wide ranges rather than converging. Under these conditions, any reported maximum likelihood estimate may be far from the true optimum. Conclusions about model adequacy are unreliable.
**Severity:** Major
**Suggested author action:** Run a global search by generating a random box of starting points spanning plausible parameter ranges and running mif2 from each. Report the best log-likelihood found across all starts.

**ID: 21.05.M3**
**Concern:** The 0.7 contact-rate multiplier in Model 3 is hard-coded, not estimated.
**Why it matters:** The stated research question is whether POMP models can estimate the change in contact rate. Model 3 imposes a fixed 70% reduction at week 22 without estimating this reduction. This means the model provides no quantitative answer to the research question. A properly specified model would include a free parameter (e.g., `phi` for the reduction factor) and estimate it.
**Severity:** Major
**Suggested author action:** Replace `0.7*Beta` with `phi*Beta` where `phi` is added to the parameter vector, given a logit transform in `parameter_trans`, and included in `rw.sd`. Then estimate phi and report a profile likelihood over it.

**ID: 21.05.M4**
**Concern:** Wrong likelihood object printed for Model 3.
**Why it matters:** The code block closing the Model 3 section prints `sir_L_pf` — the likelihood from Model 1's initial guess — rather than `sir2_L_pf`. The reported value (-1278.12, SE=6.87) is identical to Model 1's output. It is therefore unknown from the manuscript what the actual log-likelihood of Model 3 is at its initial guess.
**Severity:** Major
**Suggested author action:** Correct the print statement to `print(sir2_L_pf)` and report the actual Model 3 initial-guess log-likelihood.

**ID: 21.05.M5**
**Concern:** No profile likelihoods or confidence intervals for any parameter.
**Why it matters:** The paper's central scientific claim depends on the contact rate and its reduction. Without confidence intervals, no quantitative statement about parameter uncertainty is possible. The absence of profile likelihoods also means identifiability of parameters like Beta, eta, and rho cannot be assessed.
**Severity:** Major
**Suggested author action:** Once a global search is completed, compute a profile likelihood over the key parameter of interest (Beta or a reduction factor phi) and report a 95% confidence interval using the MCAP approach.

**ID: 21.05.M6**
**Concern:** Measurement model uses binomial, which imposes insufficient variance for weekly case counts.
**Why it matters:** Influenza surveillance counts exhibit substantial overdispersion relative to the binomial. The binomial model forces `Var(reports) = H * rho * (1 - rho)`, which typically underfits the variability in the tails of the epidemic curve. The paper acknowledges in the conclusion that a negative-binomial model is preferred (attributed to professor feedback) but does not implement it.
**Severity:** Major
**Suggested author action:** Replace `dbinom`/`rbinom` with a negative-binomial measurement model including an overdispersion parameter (e.g., `dnbinom` with size parameter). This will likely improve log-likelihoods and reduce NaN issues.

---

## Minor Points

**ID: 21.05.m1**
**Concern:** Sign convention confusion in log-likelihood comparison.
**Why it matters:** The manuscript states "the current lowest loglikelihood is around -860.9967" when -861 is better (higher, less negative) than the starting value of -7081. The word "lowest" should be "highest" (or "best"). This confusion about sign appears in the conclusion as well and may affect the reader's interpretation.
**Severity:** Minor
**Suggested author action:** Consistently use "highest log-likelihood" or "best log-likelihood" when referring to the most favorable value.

**ID: 21.05.m2**
**Concern:** NaN log-likelihoods attributed to model misspecification rather than particle degeneracy.
**Why it matters:** NaN output from the particle filter typically indicates particle collapse (all weights become zero), not model misspecification. Increasing Np is the first diagnostic step, not abandoning the model. The distinction matters for deciding what to fix next.
**Severity:** Minor
**Suggested author action:** When NaN appears, try increasing Np (e.g., to 5000 or 10000) in the mif2 call and check whether NaN frequency decreases. Report what happens.

**ID: 21.05.m3**
**Concern:** No software version information or sessionInfo().
**Why it matters:** The pomp package API changes across versions; without version pinning the results may not reproduce.
**Severity:** Minor
**Suggested author action:** Add `sessionInfo()` or `packageVersion("pomp")` output to the appendix.

**ID: 21.05.m4**
**Concern:** Deprecated R idioms in data processing code.
**Why it matters:** `funs(make.names(.))` (line 59) is deprecated in dplyr; `guides(color=FALSE)` is deprecated in ggplot2. These will generate warnings and may eventually break.
**Severity:** Minor
**Suggested author action:** Replace with `~make.names(.)` and `guides(color="none")` respectively.

**ID: 21.05.m5**
**Concern:** References are vague and incomplete.
**Why it matters:** The dataset reference lacks a download date and URL; the lecture notes reference lacks a chapter number or course year. These cannot be verified or located by a reader.
**Severity:** Minor
**Suggested author action:** Add the CDC FluView URL, access date, and specify the lecture notes (e.g., "Ionides, E. L. (2021). STATS 531 lecture notes, Chapters 11–15").
