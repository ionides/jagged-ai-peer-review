### Universal AI-only flags

Note: Only 3 reviewer files were found (Evan sub-report absent). "Universal" means raised by all 3 present reviewers.

Issues raised as Major by every reviewer that the human did not mention:

- SEIR measurement model misspecified (sd = mean rather than sqrt(mean); dmeas/rmeas variance inconsistency): raised by Alex (Finding 1, Major), Charlie (Issue 4, Major), Doug (Major 2, Major). Raised by all 3 reviewers as Major. → Universal AI-only Major flag.
- SECSDR population conservation violated (individuals lost from S without entering any compartment): raised by Alex (Finding 2, Major), Charlie (Issue 5, Major), Doug (Major 7, Major). Raised by all 3 reviewers as Major. → Universal AI-only Major flag.
- mif2/IF2 random-walk perturbation improperly calibrated, preventing optimization from exploring parameter space: raised by Alex (Finding 4, Major — rw.sd ≈ 0 for SECSDR/SEIQR), Charlie (Issue 8, Major — SEIR global search inherits rw.sd from local chain without re-specification), Doug (Major 1, Major — rw.sd = 2e-9 for SECSDR/SEIQR). Different specific model or mechanism, same logical error type. Raised by all 3 reviewers as Major. → Universal AI-only Major flag.
- SEIQR population size fixed at N = 32,000,000 instead of U.S. population (~328,000,000): raised by Alex (Finding 5, Major), Charlie (Issue 9, Major), Doug (Major 3, Major). Raised by all 3 reviewers as Major. → Universal AI-only Major flag.
- run_level set to pilot-level / inadequate computational effort for SECSDR (and inconsistent across models): raised by Alex (Finding 12, Minor), Charlie (Issue 11, Major), Doug (Major 8, Major). Raised by all 3 (Major by 2, Minor by 1). → Universal AI-only flag (near-universal as Major).
- No profile likelihood or confidence intervals for any parameter in any model: raised by Alex (Finding 14, Minor), Charlie (Issue 6, Major), Doug (Major 5, Major). Raised by all 3 (Major by 2, Minor by 1). → Universal AI-only flag (near-universal as Major).
- Missing data file (worse_hospitalization_all_locs.csv absent; reproducibility broken): raised by Alex (Finding 8, Major), Charlie (Issue 2, Major). Raised by 2 of 3 as Major (Doug does not raise this). Not universal.
- No non-mechanistic benchmark comparison (ARIMA or equivalent): raised by Charlie (Issue 3, Major), Doug (Major 4, Major). Raised by 2 of 3 as Major (Alex does not raise this; Alex Finding 7 is about cross-model likelihood comparison among the three mechanistic models, a different specific claim). Not universal.
- No quantitative goodness-of-fit or cross-model log-likelihood/AIC comparison across the three mechanistic models: raised by Alex (Finding 7, Major), Doug (Major 6, Major). Raised by 2 of 3 as Major (Charlie does not raise a separate finding on this; Charlie Issue 10 concerns convergence diagnostics, not likelihood table comparison). Not universal.
- No convergence diagnostics / model diagnostics (ESS, conditional log-likelihoods, filtering distribution): raised by Charlie (Issue 10, Major), Doug (Major 9, Major). Raised by 2 of 3 as Major. Alex Finding 6 addresses this only indirectly — its primary claim is that no local search was performed for SECSDR/SEIQR, with the absence of convergence diagnostics as a consequence, not the primary point. Not universal.
- SEIR local search excludes most parameters from optimization (mu_EI, mu_IR, tau held fixed): raised by Alex (Finding 9, Minor), Charlie (Issue 7, Major). Raised by 2 of 3 (Doug does not raise this). Not universal.
- Simulation uses hard-coded parameters rather than programmatically extracted MLE: raised by Alex (Finding 10, Minor), Charlie (Issue 13, Minor). Raised by 2 of 3 as Minor (Doug raises a related but distinct point — second-best parameter set selected — not the same specific claim). Not universal.
- SECSDR rinit hard-coded / missing E compartment: raised by Alex (Finding 13, Minor — hard-coded initial conditions, no optimizer adjustment mechanism), Doug (Major 10, Major — E compartment absent from statenames, S hardcoded). Raised by 2 of 3, with severity disagreement (Doug: Major, Alex: Minor). Charlie does not raise this. Not universal.
- References incomplete / no peer-reviewed epidemiological or statistical methods citations: raised by Charlie (Issue 15, Minor), Doug (Minor — reference list cites only student projects). Raised by 2 of 3 as Minor. Alex Finding 15 makes a different specific claim (introduction lacks literature-grounded prior ranges for parameters) and is counted as a near-miss, not a match. Not universal.

**Universal AI-only Major flags (raised as Major by all 3 reviewers, not in human issues):**
1. SEIR measurement model misspecified — sd = mean rather than sqrt(mean); dmeas and rmeas implement different variance functions.
2. SECSDR population conservation violated — individuals exit S via dN_SE but only dN_ECa ≤ dN_SE are re-entered anywhere; remainder disappear.
3. mif2/IF2 random-walk perturbation improperly calibrated — rw.sd effectively zero for SECSDR/SEIQR; SEIR global search inherits rather than re-specifies rw.sd.
4. SEIQR population size N = 32,000,000 instead of U.S. population — factor-of-10 error making parameters incomparable across models.

Count: 4 universal AI-only Major flags.
