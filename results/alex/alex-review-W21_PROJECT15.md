# Peer Review: W21 Project 15
# "An Analysis of COVID-19 Cases in Washtenaw County"

---

## Summary

This project fits a modified SEIR model with a time-varying, piecewise-constant contact rate to daily COVID-19 case counts in Washtenaw County, Michigan (March–December 2020). The authors use the pomp framework with iterated filtering (IF2) for parameter estimation, conduct a profile likelihood for the reporting rate rho, and compare the SEIR model likelihood against a negative-binomial i.i.d. benchmark and a SARMA benchmark. The project is well-organized and demonstrates familiarity with POMP methodology, but contains several meaningful methodological and analytical weaknesses detailed below.

---

## Weaknesses (Most Critical First)

### 1. [Major] ARMA Benchmark Likelihood Is Not Comparable to the SEIR Likelihood

The ARMA model is fit to the log-transformed data `log(y+1)`, and the authors adjust for the Jacobian with `arma33_s11$loglik - sum(log_cases)`. However, this Jacobian correction (`- sum(log(y+1))`) applies to the change-of-variables `log(y+1) -> y` only if the original scale were continuous. The SEIR model's likelihood is evaluated on the raw integer count scale using a discretized Gaussian measurement model. The ARMA model, by contrast, is trained on the transformed scale and produces a continuous Gaussian likelihood for `log(y+1)`. These two likelihoods are measuring fundamentally different things and are not on a comparable scale. The reported conclusion that the ARMA model (-1,104.23) outperforms the SEIR MLE (-1,151.66) conflates two incomparable likelihood surfaces, making the benchmark exercise misleading rather than informative.

**Evidence:** Lines 626-631: `arma33_s11$loglik - sum(log_cases)` is used as if Jacobian adjustment produces a likelihood on the same scale as the SEIR model, and the resulting value is directly compared.

---

### 2. [Major] mu_EI and mu_IR Are Fixed Without Justification for Not Estimating Them

Both the E-to-I transition rate (mu_EI = 0.1 day^-1) and the I-to-R transition rate (mu_IR = 0.1 day^-1) are fixed throughout all searches, including the global search, and no profile likelihood is computed for either. Fixing both rates simultaneously eliminates an important degree of freedom. The stated rationale is that the CDC incubation range supports mu_EI in [0.071, 0.5], and mu_IR is "around 0.1," but that range is quite wide. Fixing both at the same value (both = 0.1) implies equal mean durations for latency and infectiousness (both 10 days), and no sensitivity analysis explores how results change under alternative values. Fixing epidemiological parameters that are genuinely uncertain precludes learning from the data about these quantities and can bias other parameter estimates.

**Evidence:** Lines 296-317: "We will set both mu_EI and mu_IR to 0.1 and fix them during the local and global search."

---

### 3. [Major] Profile Likelihood for rho Is Underpowered and Uses Incorrect Starting Set

The profile likelihood for the reporting rate rho is constructed from guesses taken from `writeup_params.csv`, grouped by `round(rho, 2)`, keeping the top 10 by loglik. However, the profile search itself uses only one round of `mif2` for the initial `cooling.fraction.50 = 0.5` step, then two more rounds with 0.3 and 0.1. By contrast, the global search uses seven rounds of mif2 per starting point. The profile thus gets less iterated filtering than the global search, which may produce an artificially narrow or jagged profile. The authors themselves note "we would remain cautious about this result as only three points are above the threshold," acknowledging the profile is underpowered. A profile CI based on only three points above the threshold is not a reliable confidence interval.

**Evidence:** Lines 511-567: Only three mif2 calls per profile point versus seven in the global search; the CI [40.97%, 48.01%] is based on three above-threshold observations.

---

### 4. [Major] Local Search Results Table and Pairs Plots Are Suppressed (eval = FALSE)

The local search results table and both pairs plots are rendered with `eval = FALSE`, meaning they do not appear in the compiled output. These are key diagnostics for assessing whether the local search found reasonable parameter estimates before proceeding to the global search. The reader cannot verify whether local search chains converged or whether local optima were found. The trace plots for local search are shown, but without the accompanying table and scatterplot matrices the local search section is incomplete.

**Evidence:** Lines 411-419: Three code chunks set to `eval = FALSE` — the local search table and both pairs plots.

---

### 5. [Major] Initial State Values E=100, I=200 Are Ad Hoc and Unjustified

The authors initialize the exposed and infected compartments at E=100 and I=200, arguing that the first peak was caused by external population, with reference to a news report of the first travel-related case. However, there is no analysis, sensitivity check, or formal argument linking the report of a single travel case to an initial condition of 300 combined exposed/infected individuals. These values are chosen heuristically and are not estimated; they are also not profiled over. With only 367,601 total population and eta ~ 0.1 (about 36,000 susceptibles), initial seeding of 300 cases is a non-trivial perturbation that can materially affect trajectory fits, especially the first peak.

**Evidence:** Lines 214-239: "we suppose that the first peak in our data is caused by external population, and set initial value E=100 and I=200."

---

### 6. [Major] tau Is Estimated as ~0.09, but Its Interpretation Is Not Discussed

The MLE of tau from the global search is approximately 0.09 (from `writeup_params.csv`, row 1: tau ≈ 0.101). Given the measurement model variance is `(tau * H)^2 + rho * H`, a tau of ~0.09–0.10 implies that the overdispersion term `(tau*H)^2` dominates the Poisson-like term `rho*H` whenever H is large (e.g., H > ~50). The authors do not discuss what this value implies about the measurement noise relative to process noise, nor whether it is epidemiologically plausible. This is an important parameter of the observation model and deserves interpretation.

**Evidence:** `writeup_params.csv` row 1: tau = 0.101; lines 175-176 define the measurement model, but the discussion never addresses the estimated value of tau.

---

### 7. [Minor] The Measurement Model Notation Is Internally Inconsistent

The model notation in the text (line 168) specifies `Delta N_{SE} ~ Binomial(S, 1 - exp(beta * (1/N) * Delta t))` with a sign error in the exponent: the text writes `exp(beta * (1/N) * Delta t)` (positive exponent), which would give a probability greater than 1 for any positive beta. The code on line 225 correctly uses `exp(-Beta * I / N * dt)` with a negative sign. This is a transcription error in the mathematical writeup.

**Evidence:** Line 168: `\Delta N_{SE}\sim \mathrm{Binomial}(S,1-e^{\beta\frac{1}{N}\Delta t})` — the exponent lacks the factor of `-I` and the minus sign, while the C snippet at line 225 correctly implements `-Beta * I / N * dt`.

---

### 8. [Minor] No Convergence Diagnostics Beyond Trace Plots Are Presented

The analysis relies entirely on trace plots to assert convergence of the iterated filtering runs. There is no presentation of a likelihood surface showing convergence of multiple chains to the same optimum (the pairs plots for local search are suppressed). The global search pairs plots are shown, and convergence in the parameter space seems adequate, but no formal convergence metric is discussed. For instance, the spread of top-ranked likelihoods (within ~5 log-units across the top rows of `writeup_params.csv`) should be discussed in relation to Monte Carlo error.

**Evidence:** Lines 358-359: Trace plots are described but only as showing "likelihood is increasing for some of the runs, while others are stuck in local maxima." No further diagnostic is offered.

---

### 9. [Minor] The Piecewise Beta Breakpoints Are Not Epidemiologically Motivated in the Text

The five beta regimes are defined with specific date boundaries (e.g., March 24 to June 8, June 9 to June 28, etc.) but the text does not explain why these particular dates were chosen. The introduction mentions social, political, and behavioral factors but does not link specific events (lockdowns, reopenings) to the chosen breakpoints. Without this, the breakpoint choices appear arbitrary, which weakens the scientific interpretation of the estimated beta values.

**Evidence:** Lines 204-212 give the beta step function with date boundaries, but no connection to specific public health interventions or policy events is made.

---

### 10. [Minor] NCORES = 1 Means All Parallelized Computations Run Serially

The code sets `NCORES = 1L` and registers a single-core parallel backend. The `%dopar%` loops therefore run sequentially, negating the intended use of parallelism. This is likely a submission artifact (cluster jobs were cached), but it means the code as written cannot reproduce the cached results efficiently on a multicore system without user modification. A comment or explanation of the caching strategy would improve reproducibility.

**Evidence:** Line 119: `NCORES = 1L`; line 139: `cl = makeCluster(NCORES)`. All `%dopar%` loops in the global search and profile likelihood use this single-core cluster.

---

### 11. [Minor] SARMA AIC Table Is Suppressed, Preventing Verification of Model Selection

The AIC table generation for SARMA model selection (`generate_aic_table`) is in a chunk set to `eval = FALSE, echo = FALSE`, and only the minimal AIC values are reported as comments in the code (e.g., `# 231.6978, p=q=3`). The reader cannot verify that SARMA(3,3)x(1,1)_7 is indeed the best model, because neither the full AIC table nor the code output is shown.

**Evidence:** Lines 596-623: Both AIC table generation chunks are `eval = FALSE, echo = FALSE`.

---

### 12. [Minor] No Discussion of Basic Reproduction Number R0

Despite fitting a mechanistic SEIR model with time-varying beta, the authors do not compute or discuss the basic reproduction number R0 or the time-varying effective reproduction number Rt. For an SEIR model, R0 = beta * S / (mu_IR * N) in the initial susceptible population. Given that the estimated beta values (b1 through b5) are a central output of the analysis, translating these into epidemiologically interpretable R values would substantially strengthen the biological interpretation.

**Evidence:** The conclusion (lines 637-639) discusses only that "the contact rate plays an important role in the spread of virus" without computing R0 or Rt.

---

### 13. [Minor] The Reporting Rate rho Estimated at ~0.48 Is Claimed "Reasonable" Without External Validation

The authors state that the 95% CI for rho = [40.97%, 48.01%] is "a reasonable range" but do not compare this to any external estimate of COVID-19 case ascertainment in Michigan or Washtenaw County. Contemporary seroprevalence and ascertainment studies from 2020 could have been cited to evaluate whether ~45% reporting is consistent with external evidence.

**Evidence:** Line 567: "The 95% confidence interval for rho is [40.97%, 48.01%], which is a reasonable range."

---

### 14. [Minor] The Measurement Model Is Applied to H (Cumulative Recovered), Not Incidence

The state variable H accumulates all transitions from I to R between resets (via `accumvars = "H"`). This is used as a proxy for reported cases. However, cases in the data likely represent confirmed positive tests, which better corresponds to new infections (S -> E -> I) or positive test events rather than recoveries. Modeling cases as a fraction of recoveries conflates the observation process with the recovery process, and may introduce a systematic lag in the simulated cases relative to the data.

**Evidence:** Lines 176, 231, 241-259: H tracks dN_IR events, and the measurement model conditions on H. The data variable `Cases` represents confirmed new cases by report date, not recoveries.

---

### 15. [Minor] No Formal Model Diagnostics (Effective Sample Size, Filter Diagnostics)

The project does not present any particle filter diagnostics such as effective sample size (ESS) over time, which could indicate degeneracy in the filter. With NP = 1000 particles and a 306-day time series, filter collapse is a real concern, particularly around the large late-2020 outbreak where the model may struggle to track the data. Presenting ESS plots from the best pfilter run would strengthen confidence in the likelihood estimates.

**Evidence:** No ESS or filter diagnostic plots or discussion appear anywhere in the writeup.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project15/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project15/pomp_cache/writeup_params.csv` (header and first 20 rows)
