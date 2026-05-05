# Peer Review: Utah Covid Model (W21 Project 09)

## Summary

This project applies SIR-type modeling to Utah COVID-19 data from March 2020 through April 2021. The report is split into three parts: an ARIMA baseline, an attempted POMP/particle-filter SIR, and a deterministic ODE-based SIR fitted by minimizing residual sum of squares (RSS). The POMP section is almost entirely commented out, and the ODE-based SIR section follows an external tutorial rather than the course methodology. The project has substantial methodological and presentational weaknesses listed below, ordered from most to least critical.

---

## Weaknesses

### 1. POMP Model Is Essentially Abandoned (Major)

The entire particle-filter and `mif2` optimization section is commented out. The project admits "computer errors" prevented the likelihood from being computed, but no diagnostic information, alternative particle counts, or even a single `pfilter` result is shown. The section heading promises a POMP analysis but delivers only two simulation plots with hand-tuned parameter guesses. For a course centered on POMP methods, this is the most critical gap.

Evidence: Lines 211-305 of `blinded.Rmd` are wrapped in `# ...` comments. No `.rds` or `.csv` output files from any likelihood computation exist in the project folder.

---

### 2. No Likelihood-Based Inference Performed (Major)

Because the particle filter was never run successfully, no log-likelihood values are reported, no standard errors are given, and no model comparison is possible. Without a likelihood, there is no principled basis for choosing parameter values or assessing model fit. The parameter guesses (`Beta=17`, then `Beta=50`, then `Beta=200`) are explored visually without any statistical framework.

---

### 3. Deterministic ODE SIR Replaces, Rather Than Supplements, the POMP Model (Major)

The second SIR analysis uses `deSolve::ode` and L-BFGS-B minimization of RSS on cumulative case counts. This is a purely deterministic, non-probabilistic approach. It bypasses the stochastic latent-state structure that POMP modeling is designed to address. Fitting cumulative counts with RSS does not account for observation noise, reporting delays, or partial observability. The course context expects a proper POMP/SMC framework; this section is a workaround that sidesteps the core methodology.

---

### 4. Measurement Model Is Internally Inconsistent (Major)

In the POMP specification, `sir_rcovid` simulates observations as:
```r
c(Seven.day.Average = rbinom(n=1, size=H, prob=rho))
```
This uses a binomial draw from `H` (cumulative recoveries since last reset) to produce what is labeled as a seven-day rolling average of new cases. Recoveries and new cases are different quantities. The accumulator variable `H` accumulates recoveries (`dN_IR`), but new infections drive new case counts; the measurement model conflates these two flows.

Additionally, `sir_dcovid` uses a negative binomial with `mu=s`, but `s` is never defined as a state variable or parameter in `statenames` or `paramnames`. This would cause a runtime error if the code were actually executed.

---

### 5. `s` Parameter in `dmeasure` Is Undefined (Major)

`sir_dcovid` references `s` in `dnbinom(x=count, mu=s, size=theta, ...)`, but `s` is neither a state variable declared in `statenames=c("S","I","R","H")` nor a parameter in `paramnames=c("Beta","mu_IR","N","eta","rho")`. The variable name `s` (lowercase) does not match the state `S` (uppercase). This would cause an error in any actual likelihood evaluation and suggests the `dmeasure` was never successfully tested.

---

### 6. Fitting Cumulative Cases Instead of Incidence (Major)

The ODE SIR is fitted against cumulative case counts (`dat$Cumulative.Cases`) but the project's stated focus is on modeling the daily new cases (the seven-day rolling average). Fitting cumulative data with RSS severely understates discrepancy during early periods and overstates agreement during later periods. It also produces autocorrelated residuals by construction, invalidating any inference based on RSS minimization.

---

### 7. No Parameter Uncertainty Quantification (Major)

Neither the ARIMA section nor either SIR section provides confidence intervals, profile likelihoods, or any measure of parameter uncertainty. For the ODE SIR, only point estimates (`beta=0.0088`, `gamma=0.0458`) are reported with no standard errors. For ARIMA, standard errors on coefficients are printed but not discussed.

---

### 8. Particle Count and MIF Settings Are Inadequate (Minor)

In the (commented-out) local search, `Np=20` particles and `Nmif=50` iterations are used. Twenty particles is far too few for reliable likelihood estimation with a three-compartment SIR; the Monte Carlo variance would be enormous. The random-walk standard deviations (`rw.sd(Beta=500, mu_IR=0.03, rho=0.6, eta=ivp(0.07))`) are on very different scales and appear not to have been calibrated. The project should at minimum discuss why these values were chosen.

---

### 9. ACF Interpretation Is Incorrect (Minor)

The report states: "This graph shows how there is no clear lag pattern, as there is not a better acf than the unadjusted or lagged data." The ACF of the seven-day average shows very strong autocorrelation persisting for many lags (this is expected for an epidemic curve), which is the opposite of "no clear lag pattern." The ACF is not interpreted in any standard sense here; it appears the author confused a cross-correlation lag analysis with a standard ACF.

---

### 10. ARIMA Model Selection Is Not Justified (Minor)

The project selects ARIMA(5,2,4) based on the lowest AIC in the table, but does not discuss whether differencing twice (d=2) is appropriate for this data. Daily case counts that are already a seven-day rolling average are very smooth; double-differencing may over-difference and destroy signal. No unit-root test (e.g., ADF, KPSS) is reported. Additionally, the MA roots are computed only for the first two coefficients (`ma1`, `ma2`) despite the model being ARIMA(5,2,4) with four MA terms.

---

### 11. SIR Model Does Not Include Death Compartment (Minor)

The project mentions in the introduction that the SIR model "tak[es] into account the people who die at any step along the way," but neither the POMP SIR (`sir_step`) nor the ODE SIR includes a death compartment. Utah had notable COVID-19 mortality during the study period. Ignoring deaths biases both the recovery rate and the susceptible pool. The discrepancy between the stated model description and the implemented model is not acknowledged.

---

### 12. Recovery Rate Derivation Is Informal (Minor)

The recovery rate `mu_IR = 1/15` is derived by visually inspecting a `lag2.plot` of new cases vs. new recoveries and selecting the lag with the highest apparent correlation. No formal cross-correlation statistic or confidence interval is reported. Furthermore, this lag was applied as a fixed parameter rather than being estimated as part of the fitting procedure, which forfeits information.

---

### 13. Initial Conditions Are Biologically Implausible (Minor)

`sir_rinit` sets `I = 1` at day 0, regardless of the actual number of cases at the start of the time series. The data begins on March 6, 2020, with 1 confirmed case and a cumulative total of 1. While numerically plausible for the very start, the parameter `eta` (fraction susceptible) with initial value 0.05-0.07 implies that 5-7% of Utah's 3.25 million people (~162,500-227,500) were already recovered at day 0, which is inconsistent with the data showing near-zero cumulative cases at that date. This is never explained.

---

### 14. No Global Search for Parameters (Minor)

The project only performs local searches (and even those are commented out). No global search using a parameter box is shown. Without a global search, there is no evidence that the parameter estimates found correspond to a global rather than local optimum, and the geometry of the likelihood surface is entirely unknown.

---

### 15. Presentation and Writing Quality Issues (Minor)

Several issues reduce the quality of the report:
- Multiple typos throughout: "succeptable," "dieseas," "Univeristy," "diognostics," "caluclating," "spices" (for "spikes"), "acurate."
- The legend in the final SIR compartment plot is incorrectly mapped: the `scale_colour_manual` labels do not align with the lines plotted (e.g., "Susceptible" and "Infectious" are swapped relative to their visual order in the aesthetic mapping).
- The ARIMA equation shown is not the integrated (I=2) form; it omits the differencing operator.
- The `include=FALSE` chunk on line 55 hides the summary statistics that are referenced in the text, making the stated values unverifiable in the rendered output.
- The section title "Pomp" and "SIR Process" suggest two separate analyses but the relationship between them is not clearly delineated.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project09/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project09/Overview_Seven-Day Rolling Average COVID-19 Cases by Test Report Date_2021-04-19.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project09/Overview_Cumulative COVID-19 Cases with Estimated Recoveries_2021-04-19.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project09/Makefile`
