# Simulation Study Checklist (POMP-Focused)
*Adapted from Morris et al. (2019), Statistics in Medicine, with additions for POMP manuscript review*

Apply this checklist to evaluate simulation studies in statistical papers. For POMP manuscripts, simulation serves two distinct purposes that must be evaluated separately: (1) **method-comparison studies** (evaluating estimator performance) and (2) **model validation** (assessing whether the fitted mechanistic model reproduces observed data). Identify which type is present and apply the relevant sections below.

---

## Part A: Method-Comparison Simulation Studies

*(Apply when the paper evaluates estimator performance via Monte Carlo experiment)*

### 1. Aims
- [ ] **Clarity**: Objectives explicitly stated (evaluating bias, comparing methods, assessing robustness)?
- [ ] **Relevance**: Aims align with method's intended use or address literature gap?
- [ ] **Scope**: Appropriate framing (proof-of-concept vs. stress-testing vs. realistic evaluation)?

### 2. Data-Generating Mechanisms (DGMs)
- [ ] **Transparency**: DGMs fully described (parametric models, resampling procedures)?
- [ ] **Justification**: Factors varied with rationale (realism, edge cases)?
- [ ] **Design**: Factorial variation of factors? Simple and complex scenarios included?
- [ ] **Well-specified DGMs**: At least some DGMs where each method's assumptions hold? Coverage should be near nominal here — if not, something is wrong with the implementation.
- [ ] **Misspecified DGMs**: Deliberate, realistic assumption violations included? Violations varied in severity? Each method tested under both favorable and unfavorable conditions?
- [ ] **No home-court advantage**: DGMs not exclusively tailored to the proposed method's assumptions?
- [ ] **POMP-specific**: If comparing POMP inference methods (e.g., IF2 vs. PMCMC vs. ABC), do DGMs cover both low- and high-dimensional state spaces, and both weakly and strongly identifiable parameter regimes?
- [ ] **Reproducibility**: Code/data provided to regenerate datasets?

### 3. Estimands
- [ ] **Definition**: Target of inference clearly defined?
- [ ] **Alignment**: Estimands match aims (marginal vs. conditional effects)?
- [ ] **Identifiability**: Non-identifiability constraints explained if applicable?

### 4. Methods
- [ ] **Comparators**: Relevant state-of-the-art methods included?
- [ ] **Implementation**: Code provided for all methods? Convergence issues reported?
- [ ] **Fair comparison**: All methods use appropriate/default settings?
- [ ] **Failure handling**: Non-convergence and method failures documented? Failure rates reported per method × DGM?
- [ ] **POMP-specific**: For particle-filter-based methods, are the number of particles and IF2 iterations equated or otherwise fairly controlled across compared methods?

### 5. Performance Measures
- [ ] **Appropriateness**: Metrics aligned with aims (bias, SE, coverage, power, MSE)?
- [ ] **Hypothesis testing**: Type I error AND power reported?
- [ ] **Monte Carlo error**: MCSEs reported for key metrics?
- [ ] **Sample size**: n_sim justified to control MCSE?
- [ ] **Missing data**: Non-convergence/missing estimates documented and addressed?
- [ ] **POMP-specific**: Is log-likelihood estimation variance across particle filter runs reported? This contributes to total Monte Carlo error and should be accounted for.

### 6. Reproducibility & Code
- [ ] **Availability**: Scripts for data generation, analysis, and evaluation provided?
- [ ] **Random seeds**: Seeds set and stored? Parallelization streams managed?
- [ ] **Documentation**: Dependencies, software versions, computational steps detailed?
- [ ] **POMP-specific**: Are particle counts, IF2 iteration counts, and per-run random seeds recorded so stochastic results are exactly reproducible?

### 7. Reporting & Presentation
- [ ] **Structure**: Aims, DGMs, Estimands, Methods, Performance clearly sectioned (ADEMP)?
- [ ] **Clarity**: Tables/figures compare methods side-by-side? MCSEs visible?
- [ ] **Exploration**: Raw results visualized (distributions, zip plots)?
- [ ] **Limitations**: Weaknesses acknowledged (restricted DGMs, computational constraints)?

### 8. Interpretation
- [ ] **Claims supported**: No overstatement (e.g., "scalable" without large-n evidence)?
- [ ] **Generalizability**: Conclusions reflect scope of DGMs tested?
- [ ] **Fair reporting**: Competing methods fairly represented?

---

## Part B: POMP Model Validation via Simulation

*(Apply when the paper uses simulation to assess whether a fitted mechanistic model reproduces observed data — the primary use of simulation in most POMP manuscripts)*

### 9. Simulation-based model validation
- [ ] **Forward simulation**: Are trajectories simulated from the fitted model and compared to observed data?
- [ ] **Filtering distribution**: Are simulations conditioned on all observed data (filtering distribution) distinguished from unconditioned forward projections? The two serve different diagnostic purposes and should not be conflated.
- [ ] **Replicate adequacy**: Is the number of simulation replicates sufficient to produce stable summary statistics? Is Monte Carlo variability in the reported summaries negligible?
- [ ] **Summary statistics**: Are relevant summary statistics of simulated data (e.g., peak timing, total burden, seasonal amplitude) compared to observed data, not just raw trajectories?
- [ ] **Visual vs. quantitative**: Are visual trajectory comparisons supplemented by quantitative goodness-of-fit measures (log-likelihood, AIC)? Visual agreement alone is insufficient (Wheeler et al. 2024).

### 10. Particle filter diagnostics
- [ ] **Effective sample size (ESS)**: Is ESS monitored during filtering? Persistent ESS collapse indicates model-data mismatch or insufficient particles.
- [ ] **Convergence traces**: Are log-likelihood traces across IF2 iterations shown, demonstrating that optimization has converged?
- [ ] **Conditional log-likelihoods**: Are per-observation (or per-time-step) log-likelihoods plotted to identify specific periods of poor fit?
- [ ] **Particle count justification**: Is the number of particles sufficient for stable likelihood estimates? Is sensitivity to particle count assessed?

### 11. Scope of simulation scenarios
- [ ] **In-sample vs. out-of-sample**: Are simulations evaluated both within the training period and on held-out data?
- [ ] **Model robustness**: Is the model tested under outbreak dynamics or surveillance conditions outside its primary design? (Analogous to misspecification testing in Part A.)
- [ ] **Sensitivity**: Are key simulation results shown to be robust to changes in initial conditions, particle count, or random seed?

---

## Red Flags

**General:**
- Single DGM scenario only
- No comparison to baselines
- Missing MCSE or n_sim justification
- "Proof of concept" framed as comprehensive evaluation
- Competing methods configured suboptimally
- Code supplement incomplete or non-executable
- All DGMs satisfy the proposed method's assumptions (home-court advantage)
- No misspecification testing (robustness unknown)
- Proposed method wins on every metric in every scenario (suspiciously good — likely selective reporting)
- Post-hoc metric or scenario selection (ADEMP not locked before results)

**POMP-specific:**
- Filtering-distribution simulations and forward simulations conflated or not distinguished
- ESS not monitored; particle filter may be degenerating silently
- No convergence traces for IF2 or other iterative fitting algorithms
- Particle count not reported or not justified
- Model validation relies entirely on visual trajectory matching with no quantitative fit measure
- Simulation scenarios restricted to conditions closely matching the training data (no out-of-sample or stress-testing)

---

## Key References
- Morris TP, White IR, Crowther MJ (2019). Using simulation studies to evaluate statistical methods. *Statistics in Medicine* 38:2074-2102.
- Burton A, Altman DG, Royston P, Holder RL (2006). The design of simulation studies in medical statistics. *Statistics in Medicine* 25:4279-4292.
- Wheeler J, Rosengart A, Jiang Z, Tan K, Treutle N, Ionides EL (2024). Informing policy via dynamic models: Cholera in Haiti. *PLOS Computational Biology* 20(4): e1012032.
