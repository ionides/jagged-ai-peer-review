# Peer Review: W21 Project 14 — Mumps SEIR POMP Model (Michigan, 1970s)

---

## Summary

This project fits a seasonal SEIR POMP model to weekly mumps reporting data from Michigan (September 1971 – September 1973). The authors use iterated filtering (mif2) for both local and global likelihood maximization and construct a profile likelihood confidence interval for the reporting rate rho. The project is competently executed and clearly written, but contains several methodological, statistical, and presentational weaknesses detailed below.

---

## Weaknesses (Prioritized by Severity)

### 1. [Major] Measurement Model Misspecification: Negative Binomial Uses H Incorrectly

The dmeasure and rmeasure snippets use H as the "size" parameter of the negative binomial distribution:

```c
lik = dnbinom(cases, H, rho, give_log);
cases = rnbinom(H, rho);
```

In R's `dnbinom(x, size, prob)` parameterization, `size` is the dispersion parameter (a fixed positive real), not a latent state variable that changes each time step. Using H (the accumulator of recovered individuals per week) as the `size` parameter conflates a stochastic count state with a fixed overdispersion parameter. This produces a measurement model that is neither a standard negative binomial (where size is constant) nor a valid Poisson-based model. The intended construction is almost certainly `dnbinom_mu(cases, mu = rho*H, size = psi, give_log)` for some overdispersion parameter psi, or simply `dpois(cases, rho*H, give_log)`. As written, when H is small or zero the distribution is degenerate and the likelihood is ill-defined, which explains the NaN values and -Inf log-likelihoods described in the text.

---

### 2. [Major] H Is Used as Both Accumulator and Distribution Parameter — R(t) Is Never Tracked

The state vector is (S, E, I, H) rather than (S, E, I, R). H is an accumulator of daily new recoveries, reset each week via `accumvars = "H"`. There is no compartment R tracking cumulative removed individuals. This is fine for the measurement model when H is used as expected weekly cases (via a reporting rate), but because H is used directly as the `size` in dnbinom, the model is inconsistent. Furthermore, the total population constraint S + E + I + R = N is never enforced or checked; S can drift freely since there is no R compartment to absorb the removed individuals.

---

### 3. [Major] Initial Conditions for E and I Are Hard-Coded and Not Estimated

The rinit snippet fixes E = 20 and I = 10 as absolute counts regardless of N or any estimated parameter:

```c
S = nearbyint(eta*N);
E = 20;
I = 10;
H = 0;
```

These are arbitrary and never subjected to sensitivity analysis or estimation. With N = 8,881,826, fixing E and I to 20 and 10 is essentially zero relative to the population, but these choices directly affect early dynamics and can introduce systematic bias. Best practice is to treat initial infectious counts as estimated parameters (e.g., `I_0 = round(i0 * N)`) or at minimum justify the fixed values epidemiologically.

---

### 4. [Major] Global Search Reuses a Single mifs_local[[1]] Chain Rather Than Fresh mif2 Calls

The global search initializes each global run by calling `mif2(mifs_local[[1]], params = ...)`. This means all global chains inherit the tuning state (rw.sd, cooling schedule, and number of filtering iterations already run) from the first local chain, rather than starting fresh. The consequence is that the number of effective mif2 iterations in the global search equals `mumps_Nmif` plus however many iterations mifs_local[[1]] already completed. More importantly, this approach does not vary Nmif or cooling.fraction.50 for the global chains, which should generally use more iterations to escape the expanded parameter space.

---

### 5. [Major] Profile Likelihood for Rho Does Not Fix Rho During Optimization

In the profile likelihood construction, rho is included in `profile_design` but the `rw.sd` inside the profile loop does not exclude rho:

```r
rw.sd = rw.sd(b1 = 0.02, b2 = 0.02, Phi = 0.02, eta = ivp(0.02))
```

Rho is not listed in `rw.sd`, which means mif2 will not perturb rho during the profile. This is correct in intent, but the code uses `params = c(unlist(guess), mumps_fixed_params)` where `guess` includes a fixed rho value from `profile_design`. However, since rho is not given a log or logit transform in `partrans` that is applied only to estimated parameters, and since mif2 will update rho from the particle filter resampling step (not just perturbation), rho may drift away from its intended fixed value during filtering. A proper profile likelihood requires either hard-fixing rho via `fixed_params` or using a very small rw.sd for rho. The absence of explicit rho fixing is a methodological flaw.

---

### 6. [Major] mu_EI and mu_IR Are Fixed Without Justification of Rate Units

The authors fix mu_EI = 0.412 and mu_IR = 0.714. The text states the incubation period is approximately 17 days and the infectious period is "over a week." With weekly time steps and Euler integration at delta.t = 1/7 (daily sub-steps), the rates should be on a per-day scale if t is measured in weeks but delta.t = 1/7. An incubation period of 17 days corresponds to mu_EI = 1/17 ≈ 0.059 per day (or 0.412 per week ≈ 1/2.4 days), suggesting the reported value is a per-week rate. An infectious period of "over a week" at mu_IR = 0.714 per week implies mean infectious period of 1/0.714 ≈ 1.4 weeks (about 10 days), which is plausible. However, the paper gives no explicit unit derivation or citation to support these specific numeric values, making it impossible to verify whether they are correctly specified relative to the time unit used in the model.

---

### 7. [Moderate] Only a Single Simulation Is Shown for Local and Global Fit Assessment

Figures 7 and 11 each display a single simulation trajectory overlaid on data to assess model fit. A single stochastic trajectory is uninformative about whether the model characterizes the data distribution well; the trajectory might happen to match or miss by chance. Standard practice is to show an envelope of 20–100 simulations (e.g., pointwise 10th–90th percentile bands), or to use a simulation-based goodness-of-fit test. The authors acknowledge initial poor fit but do not quantify uncertainty in the final fitted simulations.

---

### 8. [Moderate] Convergence Diagnostics Are Incomplete for Global Search

The global convergence plot (Figure 8) shows considerable variability with trajectories "diverging into two directions" for rho, and the log-likelihood "cliff" shape for many chains. The authors attribute this to the curse of dimensionality but do not provide: (a) a table comparing the best global log-likelihood to the best local log-likelihood, (b) evidence that the global optimum is meaningfully better than the local optimum, or (c) discussion of whether the multimodality in rho indicates a genuine ridge or a convergence failure. Without these, it is unclear whether the global search succeeded.

---

### 9. [Moderate] Parameter Transformation Is Incomplete — b1, b2, Phi Are Unconstrained

The `partrans` argument only applies logit transforms to rho and eta:

```r
partrans = parameter_trans(logit = c("rho", "eta"))
```

Parameters b1, b2, and Phi have no enforced constraints. b2 (amplitude of seasonality) should be non-negative; Phi (phase) is meaningful only modulo 2pi. Without log or log-logit transforms on b2, the optimizer can explore negative b2 values, which are technically valid (a negative cosine amplitude is equivalent to a phase shift of pi) but create an unidentified parameterization. The global search box for b2 is [0, 5], so the boundary is honored in initialization but not enforced during mif2 perturbations.

---

### 10. [Moderate] Profile Likelihood CI Construction Uses Observed-Profile Min/Max Rather Than Wilks Inversion

The 95% confidence interval for rho is reported as the range of rho values at which `logLik > max(logLik) - 0.5 * qchisq(df=1, p=0.95)`. This is a valid application of Wilks' theorem for a profile CI. However, the implementation computes the CI by taking `min(rho)` and `max(rho)` over all points satisfying the cutoff, without fitting a smooth curve to the profile first. If the profile is noisy (as Figure 12 suggests, given that loess smoothing is applied), the raw point-wise min/max may produce a CI that is too wide or too narrow. The authors should fit the smoothed profile and invert the cutoff analytically or use the smoothed curve, not the raw points.

---

### 11. [Moderate] No Baseline Model Comparison (e.g., SIR Without Seasonality)

The paper motivates the SEIR seasonal model but never compares it formally against simpler alternatives: (1) a standard SIR model, (2) an SEIR model without seasonal forcing, or (3) even a benchmark deterministic trajectory. Without a log-likelihood comparison (e.g., via likelihood ratio test or AIC), the claim that the seasonal SEIR model is necessary and appropriate is unsupported quantitatively.

---

### 12. [Moderate] The Report Describes the Measurement Model as "Binomial" in the Text But Implements Negative Binomial

At line 127 of the Rmd: "we still use binomial process to be our measurement model." However, the dmeasure and rmeas snippets clearly use `dnbinom`/`rnbinom`, not `dbinom`/`rbinom`. This is a substantive inconsistency. If the intended model is negative binomial, the text should be corrected and the motivation for using negative binomial (overdispersion) should be explained. If binomial was intended, the code is wrong.

---

### 13. [Minor] run_level = 2 Is Hard-Coded in the Rmd

The run level controlling particle counts and iteration numbers is hard-coded to 2 throughout, with level 3 (for higher-fidelity results) never used. At run_level = 2, Np = 1000 particles are used for a 100-observation time series with 8 parameters and stochastic dynamics. While not obviously too small, the standard error of log-likelihood estimates should be reported and checked for adequacy. The paper does report logLik_se in tables, but does not comment on whether a standard error below, say, 1 unit is achieved consistently.

---

### 14. [Minor] Figure Numbering Has a Gap (Figure 9 Precedes Figure 10 But Is Placed After Figure 10 in Output)

Figure captions are numbered inconsistently: Figure 10 (sparsity illustration) appears in the report before Figure 9 (global pairwise plot) due to the tabset layout. This is a presentational error arising from the caption assignments `cap_fig10` and `cap_fig9`. A reader following figure numbers in sequence will encounter Figure 10 before Figure 9.

---

### 15. [Minor] Pairwise Plots Are Based on Only 10 Points (head(10) of Local/Global Results)

The pairwise scatter plots (Figures 6 and 9) are constructed from `r_local` and `r_global`, each reduced to the top 10 rows via `head(10)`. Ten points are far too few to reveal meaningful geometric structure in a 7-dimensional parameter space. The authors themselves note "The sampling is too sparse to give a clear picture." Using all 30 (local) or 60 (global) chain endpoints would provide more information, even if still sparse.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project14/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project14/mumps.R`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project14/mumpSEIR.c`
