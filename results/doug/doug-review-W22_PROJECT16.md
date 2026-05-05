# Peer Review: W22 Project 16
## "Modeling Covid 19 With Multivariate POMP Model"

---

## Summary

This project fits two POMP models to daily COVID-19 confirmed, death, and recovered case counts from Moscow, Russia, covering June 2020 through March 2021. The first model (SIR-CDR) is an eight-compartment structure with three simultaneous observations and a hospital-capacity threshold mechanism; the second model (SIR-D) is a simpler five-compartment structure measuring only daily deaths. The authors demonstrate intellectual ambition in attempting multivariate observation and mechanistic complexity, and they honestly acknowledge that neither model achieves adequate convergence. However, both models exhibit critical technical flaws in the process and measurement model specifications, the global search is initialized incorrectly, the profile likelihood is computed over a range that excludes the global MLE, no non-mechanistic benchmark is included, and the conclusion draws substantive scientific statements from self-acknowledged non-converged results.

---

## Major Issues

### 1. SIR-CDR measurement model: `C` and `Rr` accumulate overlapping flows, producing double-counted observations

In the SIR-CDR rprocess Csnippet (lines 244–246 of the Rmd), the accumulator `C` is updated as:
```c
C += dN_SyD + dN_SyH + rho*dN_SyR;
```
and `Rr` as:
```c
Rr += dN_HR + rho*dN_SyR;
```
The term `rho*dN_SyR` (symptomatic recoveries observed at rate rho) appears in **both** `C` (confirmed cases) and `Rr` (recovered cases) simultaneously. A single individual who recovers symptomatically is simultaneously counted as a new "confirmed case" and as a new "recovered case." In Moscow's surveillance system, confirmed cases include hospitalized and symptomatic individuals at diagnosis, not at recovery; the accumulation of `dN_SyR` into `C` is semantically incorrect. Furthermore, the same flow is added to both `Rr` and `C`, which means the same event inflates both observation channels at once. The equation for `C` in the text (line 179) states `C_{t+1} = C_t + dN_{SyH,t} + rho*dN_{SyR,t}`, but logically `dN_SyD` (symptomatic deaths) should not appear in confirmed cases unless deaths are first confirmed; the Csnippet adds `dN_SyD` to `C` while the text equation does not. This is a text-code discrepancy and an accumulator semantic error. The measurement model and accumulator logic must be reconstructed to ensure each epidemiological event is counted in exactly one observation channel.

### 2. SIR-CDR process model equation: `dN_SyH` defined twice with different rates

In the stated process model equations (lines 167 and 169), `dN_SyH` appears twice:
```
dN_{SyH} ~ Binom(Sy, 1 - exp(-mu_SyH * dt))   [line 167]
dN_{SyH} ~ Binom(Sy, 1 - exp(-mu_SyD * dt))    [line 169]
```
The second instance is clearly intended to define `dN_SyD` (symptomatic-to-death flow), not `dN_SyH`. The Csnippet correctly uses `dN_SyD` as a separate variable (line 227), but the written equations mislabel the ninth transition. This is a notation error that could confuse any reader trying to reproduce the model from the text. It should be corrected to `dN_{SyD} \sim \text{Binom}(Sy, 1-\exp{-\mu_{SyD}dt})`.

### 3. SIR-CDR capacity mechanism is implemented incorrectly and violates compartment conservation

The hospital-capacity threshold in the SIR-CDR Csnippet (lines 234–242) reads:
```c
if (Sy + H > Cap) {
  H = Cap;
  Sy -= (Sy + H - Cap);  // NOTE: H has already been updated to Cap here
} else {
  Sy -= dN_SyH;
  H += dN_SyH;
}
H += - dN_HD - dN_HR;
```
After `H = Cap`, the expression `Sy + H - Cap` evaluates to `Sy + Cap - Cap = Sy`, so the code sets `Sy -= Sy`, which zeroes out `Sy` whenever `Sy + H > Cap`. This logic does not implement a realistic capacity constraint — it eliminates the entire symptomatic compartment whenever combined occupancy exceeds capacity. Additionally, `dN_SyH` is sampled before the capacity check (line 226) but never subtracted from `Sy` in the capacity-exceeded branch, and the flows `dN_HD` and `dN_HR` are subtracted from `H` after the override, which can produce negative `H` values (since `H` may have been set to `Cap` with those individuals not yet subtracted). The authors do not report any population-conservation checks or ESS monitoring that would expose this numerical instability.

### 4. Global IF2 search initialized from a previous mif2 result object rather than the base pomp object

In the SIR-D global search (lines 528–542), the global search initializes each replicate as:
```r
mf1 %>% mif2(params=c(guess, fixed_params)) %>% mif2(Nmif=Nmif/2) -> mf
```
where `mf1 = mifs_local[[1]]` (the first local-search result, line 507). Starting the global IF2 replicates from a previous mif2 result inherits the cooling schedule of the local chain, which is already at or near its final (nearly zero) cooling state. Each global replicate therefore performs very little exploration before perturbations shrink to near zero, anchoring all replicates near the local-search solution. The reported "global maximum" may simply be the local optimum re-estimated from slightly different starting points. The fix is to replace `mf1` (a mif2 result) with the base `covid_sir` pomp object as the first argument of the global `mif2()` call (Wheeler et al. 2024, Computational adequacy).

### 5. Profile likelihood computed over a range that excludes the global MLE

The profile for `Mu_SyR` is computed over `seq(0.01, 0.95, length=Npoints_profile)` (line 609), but the global search identifies a best-fit `Mu_SyR` of well above 100 — the text states "the optimized model prefers values of above 100" (line 617). The profile grid [0.01, 0.95] excludes the global MLE by more than two orders of magnitude. As a consequence, every point on the profile is hundreds of log-likelihood units below the global maximum, the chi-squared cutoff line has no profile points above it, and no confidence interval can be extracted. The authors acknowledge this explicitly but still present the plot as an "attempted profile likelihood." This profile provides no information about parameter identifiability. The profile grid should bracket the global MLE; given the MLE is near 100, the grid should cover something like `seq(0.5, 200, length.out=Npoints_profile)` on a log scale (Wheeler et al. 2024, Parameter identifiability and uncertainty).

### 6. No non-mechanistic benchmark comparison

Neither model is compared against any non-mechanistic baseline such as ARIMA, auto-regressive negative binomial, or even a simple GARCH model. Without such a comparison, it is impossible to assess whether the proposed POMP models capture meaningful structure beyond what a parsimonious statistical model would achieve. This is the single most diagnostic check for whether mechanistic structure adds explanatory value. Wheeler et al. (2024) note that none of 32 papers in their review provided such a comparison, and that their negative binomial benchmark revealed that some mechanistic models failed to outperform it.

### 7. No quantitative goodness-of-fit metric reported for the SIR-CDR model

The SIR-CDR model is presented, its code is given, and the authors report that particle filtering produces "single-digit effective sample sizes," but no log-likelihood value is ever computed or reported. Without a numerical goodness-of-fit metric, it is impossible to assess the SIR-CDR model's fit relative to the SIR-D model or any baseline. Wheeler et al. (2024) state that "visual comparisons alone are only a weak and informal measure of goodness-of-fit"; in this case even visual comparisons are absent for the SIR-CDR model. A pfilter evaluation should be run and the log-likelihood reported, even for a poorly fitting model.

### 8. Self-diagnosed convergence failure paired with substantive parameter interpretation

The text explicitly acknowledges that the SIR-D model has not converged: global search produces diverged runs, the pairs plot shows pathological behavior, and `Mu_SyR` drifts to biologically implausible values greater than 100. Nevertheless, the paper then extracts the best-fit parameter row (line 570–572), presents it in a table, simulates trajectories from it (lines 577–590), and offers biological interpretations in the conclusion ("the *SIR-D* model measures the death cases and has separate compartments for death cases and recovered cases"). These conclusions rest entirely on a non-converged optimization. Per the `pomp-self-diagnosed-nonconvergence-audit` pattern, any result or interpretation derived from parameters the authors acknowledge as unreliable must be explicitly retracted or caveated, or the computational effort must be increased until genuine convergence is demonstrated (Wheeler et al. 2024, Computational adequacy).

### 9. SIR-D rprocess: symptomatic compartment update in overflow branch uses stale value of `Sy`

In the SIR-D Csnippet (lines 394–402), the overflow branch is:
```c
if ((dN_SyD + dN_SyR) > Sy) {
  Sy = 0;
  R += nearbyint(Sy * (dN_SyR / (dN_SyD + dN_SyR)));   // Sy is already 0 here
  D += nearbyint(Sy * (dN_SyD / (dN_SyD + dN_SyR)));   // same error
}
```
After `Sy = 0`, the expressions `nearbyint(Sy * ...)` both evaluate to zero because `Sy` has already been zeroed. The intended logic — to split the pre-zeroing value of `Sy` proportionally between R and D — requires saving `Sy` before the assignment. This means in the overflow case, neither R nor D receives any additional flow, causing both compartments to be systematically underestimated during periods when symptomatic prevalence is low. The analogous bug exists in the A-compartment overflow branch (lines 382–392). These bugs silently distort the dynamics during the epidemic's early and declining phases.

---

## Minor Issues

- **Parameter `Mu_SyR` in the SIR-CDR model is absent from `paramnames` but referenced in the text.** The text (line 128) states a parameter `mu_SyR` is present in the SIR-CDR model, but the declared `para_names` (line 193) includes `Mu_R` (a shared recovery rate) and not `Mu_SyR` as a separate parameter. The Csnippet uses `Mu_R` for symptomatic recovery (`dN_SyR`, line 223), consistent with the parameter list, but the text description at line 128 explicitly names `mu_SyR` as a distinct parameter — creating a text-code mismatch about the model's identifiability structure.

- **`partrans` in mif2 local search re-declares transformations independently from the pomp object.** The `pomp()` call for SIR-D (lines 258–265) already specifies `partrans`, but the `mif2()` call (lines 455–466) declares a separate `partrans` argument. Declaring transformations twice risks inconsistency if one copy is updated and the other is not. The `partrans` should be specified once in the `pomp()` call and not repeated in `mif2()`.

- **Fixed parameters (`Alpha=0.3`, `D_rate=0.01`) are not estimated or given profile likelihoods.** These values are fixed based on literature references, but no sensitivity analysis is performed to assess how much the results depend on these choices. Even informal sensitivity checks (repeating the global search under alternative plausible values) would strengthen the analysis.

- **`run_level=2` uses only 1000 particles (`Np=1e3`), which is very low for a model with 5 state variables.** With a 5-compartment model including stochastic epidemic dynamics, 1,000 particles is below the minimum typically recommended for stable likelihood evaluation. The resulting log-likelihood estimates carry substantial Monte Carlo error, making comparisons across global search replicates unreliable.

- **Simulation from best parameters is compared visually to data but no simulation envelope is shown.** The simulation comparison plot (lines 587–589) overlays 5 trajectories from best-fit parameters against the data, but presents no quantile envelope. A 95% simulation envelope from the filtering or predictive distribution would provide a more informative visual diagnostic.

- **The conclusion misstates the paper's primary contribution.** The abstract states the paper "tackle[s] the third point" (complex system hard to describe by differential equations), but neither model achieves meaningful fit, and the conclusion falls back to the aspiration of "potential chance to capture the complex system upon further tuning." The framing should be revised to honestly characterize the paper as an exploratory attempt with identified failure modes rather than an accomplished analysis.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/meta-skill/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-double-reset/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-semantic-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-covid-active-case-stock-flow-mismatch/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-dmeas-rmeas-scale-inconsistency/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-init-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-multiobs-stock-flow-measurement-mismatch/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-range-misalignment/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-residual-compartment-overflow/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rprocess-equation-code-discrepancy/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-self-diagnosed-nonconvergence-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-static-population-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/sarima-baseline-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project16/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project16/data/Moscow.csv`
