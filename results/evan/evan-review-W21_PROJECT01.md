# Final AI Review — w21 Project 01

## Overall Assessment

This project tackles a substantive and timely problem — modeling COVID-19 dynamics in Pennsylvania using a SEIR POMP framework with policy and vaccination covariates. The authors show genuine engagement with the mechanistic modeling process, justify their data choices carefully, and transparently acknowledge model limitations. However, the analysis has several fundamental methodological problems that prevent the results from being interpretable. The most serious is a measurement model error where the accumulator variable H is set equal to the current stock of infected individuals (H = I) rather than the flow of new infections — this misspecification affects all likelihood calculations and parameter estimates. Compounding this, no quantitative goodness-of-fit metric is reported for the POMP model, no model comparison against the ARIMA baseline is made, convergence diagnostics are absent, and the number of particles and MIF iterations are not stated. The covariate multipliers that drive the main scientific conclusions are hard-coded from assumptions rather than estimated, making those conclusions circular. With these issues unresolved, the paper's empirical claims cannot be evaluated.

---

## Key Strengths

- **Motivated data preprocessing.** The decision to exclude data before June 2020 is well-reasoned, citing testing capacity limitations and the two-peak death pattern as evidence of data quality issues.

- **Mechanistic transparency.** The step-by-step extension from SEIR to a covariate-driven model with vaccination compartment is clearly narrated, and the code is visible inline.

- **Honest acknowledgment of failure.** The authors explicitly state that "the log-likelihood has large variations," that parameters "do not converge well," and that the model is likely misspecified. This intellectual honesty is commendable.

- **Scientific contextualization.** Parameter choices are grounded in medical literature (incubation period, recovery time), providing a principled starting point even where estimation is incomplete.

---

## Major Points

**ID: 21.01.1 | Measurement model: H equals stock instead of flow**
The process model Csnippet sets `H = I` at each time step, equating H with the current number of infected individuals (a stock). The observation model then draws daily new positive case reports from H. This is a fundamental mismatch: new daily cases are a flow, not a stock. The correct formulation uses H as a cumulative-incidence accumulator — initialized to zero each observation period, incremented by `dN_EI` (or whichever transition generates observable cases) at each Euler step, and reset after each measurement. As written, the model is fitting the total current infected count as if it were daily new cases, which produces an incorrect likelihood surface. All parameter estimates derived from this model are unreliable.
*Severity: Major.*
*Suggested action: Replace `H = I` with `H += dN_EI` inside the rprocess Csnippet, add `H = 0` to the rinit function, and verify that the dmeasure function draws from H defined as new infections. Check whether the same error exists in the vaccination-extended model (`seir_step_mod_ver2`).*

---

**ID: 21.01.2 | No quantitative goodness-of-fit reported**
No log-likelihood value, AIC, or other numeric fit metric is stated for the POMP model anywhere in the manuscript. Figure 17 shows log-likelihood values on the y-axis for the global IF2 search, but these values are never quoted in the text, and no single "best" log-likelihood is identified. Without a numeric fit summary, there is no basis for evaluating whether the model is adequate or for comparing models.
*Severity: Major.*
*Suggested action: After the IF2 global search, identify the parameter vector achieving the highest log-likelihood. Run at least 10 independent replicated particle filters at that parameter vector (e.g., `replicate(10, pfilter(..., Np=5000))`), compute logmeanexp of the resulting log-likelihoods, and report this as the model's estimated log-likelihood with its Monte Carlo standard error.*

---

**ID: 21.01.3 | No quantitative comparison to ARIMA benchmark**
The ARIMA model and POMP model are assessed in separate sections with no joint comparison. The paper is silent on whether the POMP model achieves a higher likelihood or better predictive accuracy than the ARIMA benchmark. The scientific value of the mechanistic model cannot be assessed without this comparison.
*Severity: Major.*
*Suggested action: Report the best ARIMA log-likelihood alongside the best POMP log-likelihood on the same data. Note that these likelihoods are directly comparable when computed on the same observed data series. An AIC or out-of-sample prediction comparison also suffices.*

---

**ID: 21.01.4 | ARIMA AIC table misinterpreted**
The text states "we observe no significant evidence that the ARIMA model performs better than white noise." The AIC table shows AR(0) MA(0) = 751.3 and ARMA(1,0) = 240.9, a difference of over 500 AIC units. This is overwhelming evidence that autocorrelation structure exists — the opposite of the stated conclusion. This misinterpretation affects the ARIMA section conclusions and appears to have led the authors to under-utilize the ARIMA baseline.
*Severity: Major.*
*Suggested action: Revisit the AIC table interpretation. A difference of 500+ AIC units constitutes decisive evidence in favor of the AR(1) model over white noise. The ARIMA model selected (likely ARMA(2,0) or ARMA(3,0) based on AIC) should be characterized and used as the benchmark for comparison with POMP.*

---

**ID: 21.01.5 | Covariate multipliers hard-coded, making conclusions circular**
The beta multipliers (1.38 for post-September reopening, 0.89 for December restrictions) are chosen by assumption, not estimated. The conclusion that "changes in beta have a significant impact in controlling the spread of the virus" follows necessarily from the model construction, not from data. If beta is assumed to change at specific calendar dates, the model will inevitably fit those changes — this is not independent evidence for the effect of policy.
*Severity: Major.*
*Suggested action: Either estimate the covariate multipliers as free parameters in the IF2 search, allowing the data to determine their magnitude, or explicitly acknowledge that this is a confirmatory exercise demonstrating consistency rather than estimating policy effects.*

---

**ID: 21.01.6 | Convergence diagnostics absent**
No IF2 convergence trace (log-likelihood or parameter values vs. MIF iteration) is shown. Standard practice is to plot the trajectory of each parameter and the log-likelihood across iterations for multiple independent starting points. Without these traces, there is no evidence that IF2 has converged rather than stalled.
*Severity: Major.*
*Suggested action: Produce convergence trace plots using `plot(mifs_global)` or equivalent. Show at least 5–10 independent runs overlaid to assess whether they reach a common region. Also report the number of particles (Np) and MIF iterations (Nmif) used.*

---

**ID: 21.01.7 | No confidence intervals reported for any parameter**
The IF2 global search produces a scatter plot of parameter values vs. log-likelihood, and the paper reads off approximate ranges (e.g., "beta > 0.14," "rho ≈ 0.2"). These are visual impressions from a scatter plot, not confidence intervals. No profile likelihood, MCAP, or other formal CI procedure is applied. The parameters eta and mu_EI are noted as visually unidentifiable, but no formal identifiability analysis is performed.
*Severity: Major.*
*Suggested action: Compute profile likelihoods for the key parameters (Beta, rho, mu_IR) using the standard pomp workflow. Report 95% confidence intervals via the MCAP procedure or likelihood ratio cutoff. For parameters that are unidentifiable (eta, mu_EI), discuss whether fixing them affects other parameter estimates.*

---

## Minor Points

- **Vaccination compartment guard:** The code `S -= dN_SE + IM` does not prevent S from becoming negative if IM is large. Add `IM = fmin(IM, (double)S)` or equivalent before the update.

- **Reporting rate prior:** The initial simulation uses rho = 0.9 (90% reporting rate), which is implausibly high for COVID-19. The IF2 estimate of rho ≈ 0.2 is more realistic. Brief discussion of this discrepancy and what it implies for the initial simulation's validity would strengthen the paper.

- **Weekly seasonality and SARIMA:** The ACF analysis identifies weekly seasonality. The ARIMA model should either incorporate seasonal terms (SARIMA with period 7) or justify why non-seasonal ARIMA is adequate. This matters for the benchmark comparison.

- **Np and Nmif not reported:** The number of particles and MIF iterations for all filtering runs should be stated to allow reproducibility and assessment of computational adequacy.

- **mu_EI fixed or estimated:** It is unclear whether mu_EI is a fixed parameter (= 0.125) or included in the IF2 search. The text describes it as fixed from medical literature but the scatter plot appears to show variation. Clarify.

- **Accumulator variable naming:** The variable `ini_positive_remained` is used in the initial conditions but not defined in the text. Clarify what this represents.

- **Typo:** "global searcg" in the "Iterative filtering on a smaller dataset" section should be "global search."

- **Figure 12 and 16 labeling:** It is not stated whether simulated trajectories are drawn from prior parameters, posterior filtering distributions, or MLE parameters. This distinction is important for interpreting how well the model fits.
