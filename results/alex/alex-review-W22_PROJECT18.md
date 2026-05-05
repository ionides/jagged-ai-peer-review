# Peer Review: W22 Project 18 — Crude Oil Price POMP Analysis

## Summary

This project applies GARCH(1,1), ARMA, and a leverage stochastic volatility POMP model to annual crude oil prices (1980–2019). The work follows a recognizable template closely derived from a prior year's project on the Shanghai Composite Index. While the mechanics are generally executed, there are substantial weaknesses in model justification, POMP implementation correctness, result interpretation, and scientific scope that substantially limit the project's contributions.

---

## Weaknesses (Most Critical First)

### 1. [MAJOR] Corrupted Profile Likelihood CSV: Column Ordering Breaks at Row 122

The `oilprice_params.csv` file reveals that starting at row 122 (the profile likelihood section), the columns are written in a completely different order than the header. The header specifies `logLik, logLik_se, sigma_nu, mu_h, phi, sigma_eta, G_0, H_0`, but the profile rows beginning at line 122 have a different column arrangement — `phi` appears in the third column where `sigma_nu` should be, and `logLik` appears in the seventh column. This is a known bug when mixing `write.table(append=TRUE, col.names=FALSE)` calls after runs that produce differently-ordered output. All downstream analysis that reads `oilprice_params.csv` to produce the profile likelihood plot of phi is therefore based on misaligned data, invalidating the profile likelihood figure and its confidence interval interpretation.

### 2. [MAJOR] Profile Likelihood Interpretation Is Incorrect

The text states: "When phi is smaller than 0, stack of points lay above the threshold of the 95% confidence interval." The parameter phi in a stochastic volatility model is a persistence parameter constrained in (-1, 1) and in practice is expected near 1; values of phi < 0 are not substantively relevant and certainly not the region of interest. The statement suggests the authors misread their own plot. More critically, because of the column-order corruption in the CSV (Issue 1), the variable plotted on the x-axis labeled "phi" is actually a different parameter, making the conclusion doubly invalid.

### 3. [MAJOR] Annual Data Is Inappropriate for a GARCH/Volatility Model

The entire volatility modeling exercise — GARCH, and especially the leverage stochastic volatility POMP model — is designed for high-frequency financial return data (daily or at least monthly). Applying it to 40 annual observations is methodologically inappropriate. With only 39 log-return observations, there is no meaningful time-varying volatility structure to estimate; GARCH and SV models are specifically motivated by volatility clustering seen at short time scales. The authors briefly acknowledge the small sample size only as a caveat in the conclusion, but do not address the fundamental unsuitability of the model for annual data.

### 4. [MAJOR] GARCH AIC Table Is an Image, Not Reproducible Output

The GARCH AIC table (Section 3.1) is embedded as a static image (`garch.jpg`) with the actual code for computing it present but commented out (`# kable(aic_table,digits=2)`). This breaks reproducibility: readers and reviewers cannot verify the numerical values, the code exists but its output is suppressed, and the image may not match what the current code produces. This is a significant transparency and reproducibility failure.

### 5. [MAJOR] POMP Model Is Copied from a Prior Year's Project Without Adequate Adaptation

Reference [7] explicitly cites a W21 final project on the Shanghai Composite Index, and the POMP code (state names, parameter names, rproc snippets, and even variable names like `oilprice_rw.sd_rp`) is essentially a direct copy of the lecture notes template with minimal modification. There is no discussion of whether the model assumptions appropriate for equity index returns transfer to crude oil prices, no examination of alternative POMP specifications (e.g., without the leverage term), and no original modeling contribution beyond data substitution.

### 6. [MAJOR] Filtering on Simulated Data Is Uninformative Without Interpretation

Section 5.2 ("Filtering on simulated data") reports a log-likelihood of -65.07 on data simulated from the model itself. This diagnostic step, when done correctly, is meant to verify that the particle filter can recover the likelihood under known parameters. However, the project never interprets what this value means, does not compare it to what the likelihood should be under the true simulating parameters, and does not use it to assess particle filter adequacy. It is presented as a result but provides no analytic value as written.

### 7. [MAJOR] Local Search MIF2 Uses Only a Single Starting Point

The local search (Section 5.3) uses `params_test` as the sole starting parameter vector for all 20 replicate MIF2 runs. Running 20 replicates all from the same start does not constitute a local search that robustly explores the likelihood surface; it merely assesses Monte Carlo variability at one location. A proper local search should perturb the starting values across replicates to map the local landscape, as is standard in pomp-based analyses.

### 8. [MAJOR] Global Search Box Is Derived from Local Search Pairs Plot, Not Independent Reasoning

The global search parameter box in Section 5.4 is defined by reading ranges from the pairs plot of the local search results. This is circular: if the local search has not found the global maximum (which is evident given the pairs plot shows $\phi$ concentrated at 0.99, hitting the upper box constraint), then ranges derived from it may systematically exclude the true optimum. The global search should instead start from a biologically/physically motivated broad range for each parameter, with the local search results used only as a post-hoc sanity check.

### 9. [MODERATE] phi Hits the Upper Boundary of the Global Search Box

The global search box sets $\phi \in (0.98, 0.99)$, yet the local search already shows $\phi$ concentrating at 0.99 — the upper edge of the box. This indicates the optimizer is being artificially constrained and may not have found the true maximum likelihood estimate. The profile likelihood analysis is ostensibly meant to address this, but is invalidated by the column-order bug. No further investigation of whether $\phi \to 1$ (unit root in volatility) is appropriate is undertaken.

### 10. [MODERATE] ARMA(0,0) Is Dismissed Without Adequate Discussion

The AIC table in Section 4 selects ARMA(0,0) (white noise) as the best model, but the authors dismiss this because "the lowest AIC may be due to the limited size of our data" and instead proceed with ARMA(0,1). While small-sample effects are real, the white noise result is actually scientifically meaningful: it suggests annual crude oil log-returns have no autocorrelation structure, which is consistent with market efficiency. The decision to pursue ARMA(0,1) anyway, justified only by it having the second-lowest AIC, is not rigorous and could mislead readers.

### 11. [MODERATE] GARCH Log-Likelihood Comparison Is Incorrect

Section 3.2 states "Our GARCH(1,1) model has a log-likelihood of -3.331448, which will be used as a baseline for further comparison with our POMP model." However, the GARCH log-likelihood reported by `fGarch::garchFit` is on a per-observation basis, and direct numerical comparison to the POMP particle filter log-likelihood (which integrates over all observations) requires care. No such comparison is ever actually made in the results, and the claim that the POMP AIC of ~16.4 is "the lowest among all models considered" is not accompanied by the comparable GARCH or ARMA AIC values on the same scale.

### 12. [MODERATE] Convergence Diagnostics Are Not Adequately Discussed

Section 5.3 notes "some parameters could not converge very well" and Section 5.4 notes $\phi$ and $\sigma_\eta$ "seems to converge to a certain range." These are important diagnostics. The authors do not increase Nmif, increase Np, or take any corrective action to improve convergence. Stating that parameters "converge within around 50-100 iterations" for some while others do not converge is presented without any remediation or discussion of what non-convergence implies for the reliability of the MLE.

### 13. [MODERATE] No Simulation-Based Model Checking

After fitting the POMP model, the project does not simulate from the fitted model and compare simulated trajectories to the observed data. This is a standard and essential diagnostic for POMP models. The ACF of the original log-returns and residuals from the POMP fit are also never examined, making it impossible to assess whether the SV model provides a better characterization of the data than ARMA or GARCH.

### 14. [MINOR] Data Subsetting Row Indexing Is Fragile and Undocumented

The code `selected_oil = oil[120:160,]` uses hard-coded row indices to select 1980-2020 data. There is no verification that these indices correspond to the intended years, and the comment says "forty years' data" but the code selects 41 rows. The text states the analysis excludes 2020 due to COVID-19, but it is not verified that row 160 is not 2020.

### 15. [MINOR] Research Question Is Overly Broad and Not Answered

The stated research question — "Can we use time series analysis to analyze crude oil prices?" — is trivially answered by the existence of the analysis itself. A more precise question (e.g., "Does a leverage stochastic volatility model provide a better description of annual crude oil price volatility than GARCH(1,1)?") would focus the project. The conclusion does not circle back to answer even the broad question in a substantive way; it merely summarizes that models were fit.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project18/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project18/crude-oil-prices.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project18/oilprice_params.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project18/Makefile`
