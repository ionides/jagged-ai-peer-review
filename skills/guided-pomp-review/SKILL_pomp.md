---
name: peer-review-pomp
description: Generate rigorous, evidence-based peer reviews for statistical and methodological papers, with specialized depth for POMP (partially observed Markov process) manuscripts. Use when asked to review a manuscript, evaluate a statistical paper, write referee comments, or assess methodological research — especially papers fitting mechanistic models to time series data. Produces structured reviews with Summary, Major Issues, and Minor Issues sections. Includes specialized checklists for POMP best practices (Wheeler et al. 2024), simulation studies (Morris et al. 2019), and code/data supplements. Always outputs reviews using the provided Quarto template.
---

# Statistical Peer Review Skill (POMP-Focused)

Generate rigorous, evidence-based peer reviews for statistical and methodological papers, with specialized depth for POMP manuscripts.

## Workflow

1. **Read the manuscript** carefully, creating a scratchpad of issues organized by section
2. **Identify paper type**: if the paper fits a mechanistic model to time series data using POMP methods, apply the POMP checklist below *in addition to* the general criteria
3. **Apply checklists** from `references/` for simulation studies and code supplements if present
4. **Research** relevant literature on the web to verify claims and find context
5. **Create review** using the Quarto template in `assets/rev_template.qmd`
6. **Output** the review as a `.qmd` file

---

## Review Structure

Every review must have three sections:

### 1. Summary
- State paper's goals, methods, and claims in 2-3 sentences
- List key strengths (novel algorithms, code availability, well-designed simulations)
- State major weaknesses upfront (unsupported claims, missing comparisons, poor reproducibility)
- Example opener: *"The paper proposes [method]. While [strength], the evaluation is incomplete and [weakness]..."*

### 2. Major Issues
Use descriptive headings (e.g., "**Exaggerated scalability claims**"). For each issue:
- Cite specific page, equation, table, figure, or code line
- Contrast with prior work where relevant
- Propose actionable fixes

### 3. Minor Issues
Bullet points for:
- Notation inconsistencies
- Unclear language
- Minor unsupported claims
- Typos, figure readability
- Code quality issues

---

## Evaluation Criteria

Assess against five dimensions:

| Criterion | Key Questions |
|-----------|--------------|
| **Methodology** | Appropriate techniques? Identifiability? Convergence proofs? |
| **Reproducibility** | Code quality? Documentation? Dependencies managed? |
| **Empirical Claims** | Sufficient power? Appropriate baselines? Effect sizes reported? |
| **Scholarly Integrity** | Citation gaps? Overstated novelty? Misrepresented prior work? |
| **Presentation** | Consistent notation? Readable figures? Clear writing? |

---

## POMP-Specific Checklist

When the paper fits a mechanistic model to time series data, work through each item below. For each item, note whether the manuscript **satisfies**, **partially satisfies**, or **fails** the practice. Items that could threaten the validity of conclusions → **Major Issues**. Items unlikely to affect main conclusions → **Minor Issues**. Cite the relevant recommendation from Wheeler et al. (2024) when raising a point.

**Reference:** Wheeler J, Rosengart A, Jiang Z, Tan K, Treutle N, Ionides EL (2024). Informing policy via dynamic models: Cholera in Haiti. *PLOS Computational Biology* 20(4): e1012032. https://doi.org/10.1371/journal.pcbi.1012032

The Wheeler et al. manuscript and supplementary information are available in `../wheeler24/` (`ms.txt`, `ms.pdf`, `si.txt`, `si.pdf`). Revisit these as needed.

### Quick-priority items (check these first)

When time is limited, focus on:
1. **Benchmark comparison** (#2) — the single most diagnostic check for whether a model captures meaningful structure
2. **Quantitative goodness-of-fit** (#3) — without numbers, model adequacy cannot be assessed
3. **Computational adequacy** (#6) — insufficient computation can make a good model look bad
4. **Parameter identifiability** (#5) — unidentifiable parameters undermine all conclusions
5. **Forecast methodology** (#7) — directly relevant when models are used for policy

---

### 1. Likelihood-based inference or rigorous alternative

**Practice:** Parameters should be estimated by maximizing the likelihood, or by a rigorous alternative (Bayesian inference with proper likelihood accounting). Ad hoc calibration (moment matching, eyeball fitting, fitting to summary statistics) is less reliable and makes formal model comparison difficult.

**What to look for:**
- Is the likelihood function defined and evaluated?
- For stochastic models: are plug-and-play methods used (particle filter + iterated filtering, PMCMC, etc.)?
- For deterministic models: is least squares on an appropriate scale used, or an explicit measurement model specified?
- Are alternative fitting approaches (ABC, simulated method of moments) justified if used?

---

### 2. Benchmark comparison

**Practice:** Mechanistic models should be compared against non-mechanistic statistical benchmarks (e.g., ARMA, auto-regressive negative binomial). This provides an objective baseline for whether the mechanistic model captures meaningful structure.

**What to look for:**
- Is the mechanistic model's fit compared to any non-mechanistic benchmark?
- Is the comparison quantitative (log-likelihood or AIC)?
- For spatiotemporal models: are per-unit comparisons made, not just aggregate?

**Wheeler et al. context:** None of the 32 papers in their Haiti cholera literature review performed such a comparison. Their auto-regressive negative binomial benchmark revealed that some models failed to beat it; per-department comparisons exposed that Model 3 underperformed in the departments with the most cases.

---

### 3. Quantitative goodness-of-fit reporting

**Practice:** Published models must present quantitative measures of goodness-of-fit (log-likelihood, AIC, or comparable metrics), not just visual comparisons of simulations to data.

**What to look for:**
- Are log-likelihood values reported?
- Are AIC or similar information criteria used for model comparison?
- Is the comparison on the same data and observation model so values are directly comparable?
- Are visual comparisons supplemented by quantitative measures?

**Wheeler et al. context:** "Visual comparisons alone are only a weak and informal measure of goodness-of-fit." Models that looked visually reasonable had substantially lower likelihoods than achievable with the same model structures.

---

### 4. Model diagnostics

**Practice:** Beyond overall goodness-of-fit, diagnostic tools should be applied to understand where and how the model succeeds or fails.

**What to look for:**
- **Conditional log-likelihoods**: are per-observation log-likelihoods plotted to identify periods of poor fit?
- **Effective sample size**: for particle filter inference, is ESS monitored?
- **Filtering distribution**: are simulations conditioned on observed data compared to forward simulations from initial conditions?
- **Hidden states**: are reconstructed latent variables examined for plausibility?
- **Summary statistics**: are summary statistics of simulated data compared to observed data?

**Wheeler et al. context:** Conditional log-likelihood plots led to discovery that Model 3 could not explain the cholera surge during Hurricane Matthew, motivating hurricane parameters. Filtering-distribution comparisons revealed that Model 3's calibrated parameters predicted larger outbreaks than observed, indicating misspecification.

---

### 5. Parameter identifiability and uncertainty

**Practice:** Profile likelihoods should be computed to assess whether parameters are identifiable from the data. Confidence intervals should be reported.

**What to look for:**
- Are profile likelihoods computed for key parameters?
- Are confidence intervals reported (e.g., via Monte Carlo Adjusted Profile, MCAP)?
- Are implausible parameter estimates flagged as potential signs of model misspecification?
- Is confounding between collinear covariates discussed?

**Wheeler et al. context:** For Model 2, the MLE for immunity loss rate was zero (infinite immunity) and human-to-human transmission was also zero — interpreted as evidence of model misspecification, not biological truths.

---

### 6. Computational adequacy

**Practice:** Numerical optimization and likelihood evaluation must be performed with sufficient computational effort. Convergence diagnostics should be presented.

**What to look for:**
- Is there evidence of convergence (multiple searches from different starting points reaching similar likelihoods)?
- Are the number of particles, iterations, and search replicates reported?
- Are standard IF2/particle filter diagnostics shown (convergence traces, log-likelihood traces)?
- Is there evidence that increasing computational effort was explored?

**Wheeler et al. context:** The large improvement in Model 1's log-likelihood was "primarily attributed to increasing the computational effort" in numerical maximization. Profile likelihood calculations for Model 3 required 28,938 CPU-hours across 7,568 parallel jobs.

---

### 7. Forecast methodology

**Practice:** Forecasts should be generated by simulating forward from the filtering distribution (conditioning on all observed data up to the forecast origin), not merely from estimated initial conditions. Parameter uncertainty should be propagated into forecast uncertainty.

**What to look for:**
- Are forecasts conditioned on recent data via the filtering distribution?
- Is parameter uncertainty accounted for in forecast intervals?
- For deterministic models: is the inability to condition on recent data acknowledged as a limitation?
- Are forecast intervals calibrated?

**Wheeler et al. context:** Deterministic models cannot easily condition forecasts on recent data, leading to overconfident forecasts. For stochastic models, forward simulation from the filtering distribution is demonstrated along with both Bayesian and frequentist approaches for propagating parameter uncertainty.

---

### 8. Model variations and nested comparisons

**Practice:** Scientifically motivated model variations should be tested systematically. Nested models can be compared via likelihood ratio tests. Adding or removing features should be evaluated for statistical support.

**What to look for:**
- Are alternative model structures considered and compared?
- Are nested model comparisons performed using likelihood ratio tests or AIC?
- Are model variations scientifically motivated (not data-dredging)?
- Is there evidence of iterative model development guided by diagnostics?

---

### 9. Stochasticity

**Practice:** Stochastic models are generally preferred over deterministic models for biological systems. Both process noise and measurement noise should be considered. Overdispersion in the measurement model is often needed.

**What to look for:**
- Does the model include process noise (environmental and/or demographic stochasticity)?
- Is the measurement model overdispersed (e.g., negative binomial rather than Poisson)?
- If a deterministic process model is used, is this simplification justified?

**Wheeler et al. context:** Fitting a deterministic model to stochastic data distorted parameter estimates because unmodeled stochastic variation was absorbed by other parameters. Models 1 and 3 use multiplicative gamma white noise in transmission. The measurement model uses negative binomial distributions for overdispersion.

---

### 10. Reproducibility and extendability

**Practice:** Code, data, and final parameter values should be published. The analysis should be structured so others can reproduce, question, and extend the results.

**What to look for:**
- Is source code publicly archived (e.g., with a DOI)?
- Are final parameter estimates published (not just code to re-run)?
- Are all necessary data files included (main dataset plus auxiliary matrices, covariates, etc.)?
- Does the code actually run? Does the measurement model in code match the text?

**Wheeler et al. context:** Model 2 was a cautionary example: code available but missing data files, variable-naming errors, and measurement model discrepancies between code and text. Model 3 was the gold standard: code archived with DOI, final parameters in supplementary material.

---

### 11. Corroboration with scientific knowledge

**Practice:** Fitted results (parameter estimates, reconstructed latent variables) should be checked for consistency with independent scientific knowledge. Implausible estimates may indicate model misspecification rather than new scientific findings.

**What to look for:**
- Are estimated parameter values compared to independent evidence (e.g., known disease natural history)?
- Are reconstructed latent variables (e.g., susceptible fraction, force of infection) checked for biological plausibility?
- Are surprising parameter estimates interpreted cautiously?

---

### 12. Measurement model specification

**Practice:** The measurement model (observation process) should be carefully specified, accounting for reporting rates, reporting delays, overdispersion, and other features of the observation process.

**What to look for:**
- Is the reporting rate estimated or fixed? If fixed, is the value justified?
- Is overdispersion modeled (negative binomial, log-normal, etc.)?
- Are reporting artifacts (e.g., day-of-week effects, changes in surveillance) considered?
- Does the measurement model in code match the mathematical description?

---

### 13. Initial conditions

**Practice:** Initial values can substantially affect model fit and should be estimated or justified. Sensitivity to initial conditions should be assessed.

**What to look for:**
- Are initial conditions estimated as parameters or fixed?
- If fixed, is sensitivity to initial conditions assessed?
- For spatiotemporal models: are per-unit initializations handled appropriately?

**Wheeler et al. context:** The choice of initialization strategy affected AIC by ~72 units for Model 2. For Model 3, departments with zero initial case counts required estimating (rather than fixing) initial infected counts.

---

## Tone Guidelines

- **Direct but collegial**: Use *"The authors fail to address..."* not *"It might be helpful to consider..."*
- **Technically precise**: Reference equations, code, prior work to ground critiques
- **Constructive**: Every criticism should include a path to resolution
- **Fair**: Acknowledge genuine contributions; don't dismiss good work over minor flaws

---

## Specialized Checklists

For papers with simulation studies, apply: `references/simulation-study-checklist.md`

**For papers with simulation studies**: Also invoke the `setup-benchmark` skill (via the Skill tool) to gain access to deep domain knowledge on Monte Carlo experiment design. This enables you to evaluate:
- Whether DGPs include both well-specified and deliberately misspecified settings (not just "home-court" scenarios)
- Whether coverage diagnostics are adequate (SE ratio, bias-eliminated coverage)
- Whether Monte Carlo SEs are reported and sufficient
- Whether the DGP design is factorial, space-filling, or unjustifiably narrow
- Whether truth functions satisfy identifiability constraints
- Whether practical significance thresholds are pre-specified
- Red flags from the study-design literature (Niessl et al. 2022, Morris et al. 2019)

For papers with code/data supplements, apply: `references/code-supplement-checklist.md`

---

## Output Format

Always use the Quarto template at `assets/rev_template.qmd`:
1. Copy template to working directory
2. Update YAML frontmatter (title with manuscript ID, subtitle with paper title)
3. Write review content in the template structure
4. Output as `.qmd` file

---

## Common Critique Patterns

**General:**

**Unsubstantiated claims**: *"The authors claim [X] (p.Y) but provide no evidence. The cited results show [contrary finding]."*

**Missing comparisons**: *"No comparison to [standard method] is included, making it impossible to assess practical utility."*

**Reproducibility gaps**: *"The supplement omits [simulation/analysis] code; results cannot be verified."*

**Misspecified baselines**: *"The comparison to [method] uses non-default/suboptimal settings (line X), unfairly disadvantaging it."*

**Overstated novelty**: *"The proposed [technique] is equivalent to [prior work] with minor modifications."*

**POMP-specific:**

**No benchmark**: *"The mechanistic model is not compared against any non-mechanistic benchmark (e.g., ARMA, auto-regressive negative binomial). Without such a comparison, it is impossible to assess whether the model captures meaningful structure beyond what a simple statistical model would achieve. See Wheeler et al. (2024), §Model diagnostics."*

**Visual-only fit assessment**: *"Goodness-of-fit is assessed only visually. Log-likelihood or AIC values must be reported for any meaningful model comparison. Wheeler et al. (2024) note that visual comparisons are 'only a weak and informal measure of goodness-of-fit.'"*

**Insufficient computation**: *"No evidence of convergence is presented (e.g., likelihood traces, replicate searches from diverse starting values). Reported likelihoods may not be near the MLE, undermining all downstream conclusions. See Wheeler et al. (2024), §Computational adequacy."*

**Ad hoc calibration**: *"Parameters are calibrated by [method] rather than likelihood maximization, making formal model comparison and uncertainty quantification impossible."*

**Forecast from initial conditions only**: *"Forecasts are generated from estimated initial conditions rather than the filtering distribution. This ignores information in recent data and will produce overconfident, poorly calibrated forecast intervals. See Wheeler et al. (2024), §Forecasts."*

**No profile likelihoods**: *"Profile likelihoods are not reported for key parameters. Without these, it is unclear whether parameters are identifiable from the data, and the reported point estimates may be unreliable."*
