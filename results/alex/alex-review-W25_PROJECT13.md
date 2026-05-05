# Peer Review: W25 Project 13 — Statistical Modeling of Kepler Light Curves for Exoplanet Detection

---

## Summary

This project applies a POMP framework to Kepler mission light-curve data, combining a boxcar transit model with an Ornstein-Uhlenbeck (OU) process to detect an exoplanet transit signal for star kepid 892376. Optimization is carried out with DEoptim. The conceptual direction is sound and the application domain is interesting, but the project contains numerous critical methodological and reporting flaws that undermine confidence in the results.

---

## Weaknesses (Most Critical First)

### 1. [CRITICAL] Log-likelihood values are explicitly fabricated

In the Inference and Optimization section the text states: *"Note: I made up these numbers based on typical patterns—swap in your actual log-likelihood values if you have them!"* The two reported log-likelihood values (−129990.15 at Iteration 1 and −151017.16 at Iteration 36) are acknowledged fabrications. This is a fundamental breach of scientific reporting. Any conclusions derived from or supported by these numbers are unfounded.

**Evidence:** `blinded.Rmd` lines 487–490; confirmed in `blinded.html` pre-blocks.

---

### 2. [CRITICAL] Log-likelihood decreases rather than improves across iterations

Even if the reported numbers were real, the "optimization" shows the log-likelihood moving from −129990 (Iteration 1) to −151017 (Iteration 36). Because the goal is to *maximize* the log-likelihood (or equivalently minimize the negative log-likelihood), a more negative value at Iteration 36 represents a *worse* fit. The narrative claims "a big jump!" of improvement, which is the opposite of the truth. This error demonstrates a fundamental misunderstanding of likelihood-based inference.

**Evidence:** `blinded.Rmd` lines 487–490; the text narrative in the Inference section.

---

### 3. [CRITICAL] The POMP model uses a fixed time step of delta.t = 1, which is likely mismatched with the data's time resolution

The OU process is discretized with `delta.t = 1` in `euler(ou_step, delta.t = 1)` (line 284), and the C snippet hard-codes `delta_t = 1.0`. However, the Kepler data has observations every ~0.02 days (~29-minute cadence, as seen in Statistics.csv). Using a step size of 1 day means the particle filter will skip enormous portions of the observation timeline, destroying the intended autocorrelation structure of the OU process. The OU step formula requires dt to match actual elapsed time; the hard-coded value of 1 produces a fundamentally wrong transition density.

**Evidence:** `blinded.Rmd` lines 327–332 (`ou_step` C snippet); Statistics.csv time column (spacing ~0.020 days).

---

### 4. [CRITICAL] Disposition for the target TCE is "Unknown", not "CANDIDATE" — validation is uninformative

The HTML output clearly shows: `TCE 1 (Planet 1): Estimated p = 0.46, Disposition = Unknown`. Throughout the Results and Discussion sections the paper claims the TCE disposition is "CANDIDATE" and uses this to justify confidence in the detection. The code's own output contradicts this claim, suggesting either the KOI matching failed or the target TCE is not in the KOI catalog. The scientific conclusion rests on an unverified premise.

**Evidence:** HTML pre-block 4; `blinded.Rmd` lines 506–511; Results section text at lines 630–631.

---

### 5. [CRITICAL] p_1 is a fixed scaling factor, not a probability — its interpretation is incorrect

The parameter p_1 is bounded between 0.01 and 1 and multiplies the transit depth in the boxcar model (`flux_pred -= p_1 * delta_1`). It is a depth-scaling factor, not a "probability of the transit being a true exoplanet signal." The model structure provides no probabilistic interpretation for p_1 as a detection probability; it merely rescales the transit depth. The validation plot and discussion treat the estimated value (~0.46) as a transit probability, which is a category error.

**Evidence:** `blinded.Rmd` lines 297–300 (C snippet), lines 391–396 (bounds), lines 563 and 630–631 (interpretation); discussion at line 737.

---

### 6. [MAJOR] The "preliminary plot" compares raw and quality-filtered data but labels them misleadingly

The code at lines 127–158 plots "Raw" (all TIME points including NA flux rows) and "Processed" (quality == 0, non-NA rows). No normalization or detrending has been applied to the "Processed" series at that point in the code — the detrending happens later in the `flux` chunk (lines 162–180). The figure caption and surrounding text imply the processed data is the final detrended product, but it is only quality-filtered. This confuses the reader about how preprocessing actually unfolds.

**Evidence:** `blinded.Rmd` lines 126–180; code order in setup chunk vs. flux chunk.

---

### 7. [MAJOR] Absolute file paths are hard-coded to a specific user's machine

Data are loaded from `/home/ppratik/ondemand/*.csv`. These paths are non-portable; the project cannot be reproduced by anyone else without manual intervention. The CSV files are present in the project folder, but the code does not use relative or dynamically determined paths. This also constitutes a potential reproducibility failure.

**Evidence:** `blinded.Rmd` lines 43–46.

---

### 8. [MAJOR] The batman Python package is imported but never used

Lines 38–40 configure a Python environment and import the `batman` transit modeling package. The package is never called anywhere else in the code; all transit modeling is done via the boxcar C snippet. The import is vestigial and will cause the document to fail to compile on any machine without Python and batman installed, introducing an unnecessary dependency.

**Evidence:** `blinded.Rmd` lines 38–40; no other reference to `batman` anywhere in the file.

---

### 9. [MAJOR] No uncertainty quantification is provided for any estimated parameter

The project reports point estimates from DEoptim but provides no confidence intervals, profile likelihood plots, bootstrap uncertainty, or posterior distributions. Given the stochastic nature of DEoptim (acknowledged in the README), multiple optimization runs will yield different parameters. Without uncertainty measures, it is impossible to assess whether the estimated period (11.2 days), depth (0.12), or duration (5.4 days) are precisely determined or highly uncertain.

**Evidence:** `blinded.Rmd` entire Results section (lines 548–729); README.rtf acknowledging stochastic variability.

---

### 10. [MAJOR] The estimated transit duration (5.44 days) is physically implausible given the period (11.2 days)

The boxcar model estimates a transit duration of ~5.44 days and period of ~11.2 days. This means the planet would be in transit for roughly 48% of its orbit. For any realistic stellar system, transit durations are a small fraction of the orbital period (typically hours, not days). The discussion presents this as a credible result ("consistent with a moderately long transit event") without flagging the obvious physical implausibility. This suggests the optimizer has converged to a degenerate solution rather than a true transit.

**Evidence:** `blinded.Rmd` lines 556–558 (parameter table), lines 563–564 (interpretation).

---

### 11. [MAJOR] Results section mentions an orbital period of "approximately 32 days" but the estimated period is 11.2 days

The concluding paragraph of the Results section states "a long-period planet with an orbital period of approximately 32 days" while the estimated P_1 is 11.20929925 days. This internal inconsistency — the wrong value cited in a different part of the same section — suggests parts of the text were written for a different star or a different optimization run without proofreading.

**Evidence:** `blinded.Rmd` line 729 vs. line 556.

---

### 12. [MODERATE] kepid selection is fragile and not reproducible to the stated star

The code selects the kepid by finding the first star in TCE.csv with more than one TCE (lines 66–72). This approach is non-deterministic with respect to data ordering and does not guarantee kepid 892376 will always be selected. The paper claims to study kepid 892376, but the code may select a different star on a different system if TCE.csv row ordering differs. The selection should be explicit.

**Evidence:** `blinded.Rmd` lines 66–72.

---

### 13. [MODERATE] The particle filter uses only Np = 1000 particles, which is very low for a dataset of ~71,000 observations

Statistics.csv contains ~71,427 rows. After quality filtering, the time series is still very long. With only 1000 particles the filter variance will be large, producing noisy likelihood estimates. For DEoptim to navigate the likelihood surface reliably, each function evaluation must return a stable log-likelihood value, which is not achievable with so few particles on a time series of this length.

**Evidence:** `blinded.Rmd` line 379 (`Np = 1000`); Statistics.csv has 71,428 rows.

---

### 14. [MODERATE] Residuals are computed using a single stochastic OU draw, not the posterior mean or expected value

The `compute_flux_pred` function (lines 515–543) simulates one trajectory of the OU process. Residuals calculated against this single random draw will have an additional stochastic component unrelated to model fit. Proper residual analysis for a POMP model requires either filtering-based expected state estimates (e.g., from `pfilter`) or repeated simulations averaged together, not a single sample path.

**Evidence:** `blinded.Rmd` lines 515–543, 593–601.

---

### 15. [MINOR] Writing quality is poor throughout, with numerous typos and informal language

The document contains pervasive typographical errors ("starlite," "lite curves," "dorm" for "dnorm," "indicant," "depf," "frum," "bi," "cud," "mor"), informal phrasing ("This is super important," "It's fantastic," "crazy outliers"), inconsistent figure references (figures claimed in prose that do not match the code), and second-person address mixed with third-person narration ("In your implementation"). These issues substantially reduce the professional quality of the report.

**Evidence:** Multiple locations throughout `blinded.Rmd` (e.g., lines 15, 462, 468, 479, 563, 575, 716, 729).

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project13/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project13/blinded.html`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project13/Statistics.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project13/TCE.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project13/KOI.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project13/false_positive.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project13/README.rtf`
