# Final AI Review — 25.14
## Nova Scotia's Influenza Cases (STATS 531, W25)

> Challenge skipped — Grounding signal was Strong. All major claims in the first-pass review were directly supported by manuscript text and code.

---

## Overall Assessment

This project demonstrates solid engagement with the POMP framework, fitting three compartmental models (SIR, SIRS, SEIRS) to weekly lab-confirmed influenza data from Nova Scotia using mif2 global and local searches, particle filtering, and profile likelihood. The SEIRS model, with the highest log-likelihood and a seasonal forcing term, is a reasonable best model. The project includes positive features: negative binomial measurement noise in SIR and SEIRS, ESS monitoring, multiple starting points in global search, and profile likelihood for the reporting rate. However, several methodological problems undermine the reliability of the reported conclusions. The final model comparison uses single particle filter evaluations rather than replicated logmeanexp estimates, which renders the SIRS log-likelihood in the conclusion table unreliable. The SIRS model uses Poisson measurement noise while the other two models use Negative Binomial, making the three-way log-likelihood comparison invalid on its face. SIRS parameter estimates are biologically implausible (population N ≈ 325 million, recovery rate implying a 1-day infectious period), indicating model misspecification that is not diagnosed. The profile likelihood for rho collapses to a degenerate confidence interval (min = max), suggesting a numerical failure that is not acknowledged. These issues collectively weaken the comparative conclusions, though the SEIRS analysis itself is the most careful and largely sound.

---

## Key Strengths

**25.14.S1 — Negative Binomial measurement model (SIR, SEIRS)**
The SIR and SEIRS models use `dnbinom_mu` with a dispersion parameter k, appropriately accommodating overdispersion in the weekly influenza counts. This is methodologically sound and reflects the empirical distribution (right-skewed, zero-inflated). Confidence: High.

**25.14.S2 — Multiple starting points in global search**
Both SIR (20 chains) and SEIRS (100 chains) run global searches over a broad parameter space using mif2, reducing the risk of settling in local optima. The pair plots comparing initial guesses and fitted values demonstrate that mif2 successfully moved parameters toward higher likelihoods. Confidence: High.

**25.14.S3 — Profile likelihood over rho for SEIRS**
The project computes a profile likelihood over the reporting rate rho, correctly holding other parameters at their optimized values for each fixed rho. This is an appropriate identifiability analysis. The discovery that the best-fit rho from global search lies outside the profile CI is a useful diagnostic finding. Confidence: Moderate (the numerical execution has problems, but the approach is correct).

**25.14.S4 — ESS monitoring**
Effective sample size is tracked and reported for the SEIRS particle filter, with the finding that ESS drops at each seasonal cycle onset but remains above zero. This is good practice. Confidence: High.

---

## Major Points

**25.14.1 — Single pfilter used for final model comparison**
Severity: Major

The conclusion compares models using single `logLik(pfilter(...))` calls:
```r
loglik_sir  <- logLik(pfilter(mif_sir, Np = 2000))
loglik_seir <- logLik(pfilter(mif_seirs, Np = 2000))
loglik_sirs <- logLik(pfilter(mif_sirs, Np = 2000))
```
Each is a single Monte Carlo estimate. The SIRS value shown (-19747) is dramatically lower than the SIRS local-search best (-2470), almost certainly because this pfilter was run at a poor parameter value or without averaging. The SEIRS value (-591.7) also differs from the best global-search value (-586.6). These inconsistencies confirm that the reported comparison table is unreliable.

Suggested author action: Replace each single pfilter call with `logmeanexp(replicate(20, logLik(pfilter(mf, Np=2000))), se=TRUE)` run at the best-fit parameters for each model. Report the SE alongside each estimate.

**25.14.2 — SIRS measurement model inconsistency (Poisson vs. Negative Binomial)**
Severity: Major

The SIRS model uses Poisson measurement noise (`rpois`, `dpois`) while SIR and SEIRS use Negative Binomial. Poisson noise has no free overdispersion parameter, structurally constraining the SIRS model relative to the others. Because the models differ in both structure and measurement family, log-likelihood values are not comparable on a level playing field. The right-skewed, zero-heavy data strongly favors overdispersed models.

Suggested author action: Replace the SIRS measurement model with Negative Binomial (add dispersion parameter k), consistent with SIR and SEIRS. Rerun the SIRS fitting and update the comparison.

**25.14.3 — SIRS parameters biologically implausible; misspecification not diagnosed**
Severity: Major

The best SIRS local-search estimates include:
- `mu_IR ≈ 8.0`: average infectious period = 1/8 week ≈ 1 day (influenza typical: 4–7 days)
- `N ≈ 325 million`: exceeds Canada's total population; Nova Scotia has ~970,000 people
- `rho ≈ 4.3e-6`: one reported case per ~230,000 infections

These are strong signals of model misspecification or unidentifiability. The text acknowledges poor fit but does not connect it to these parameter pathologies.

Suggested author action: Constrain N to the Nova Scotia population (fix at 969,400 or bound tightly). Compute profile likelihoods over mu_IR and compare estimated values to the Anderson and May (1991) reference cited in the paper. Flag the estimates as evidence of misspecification rather than attributing all SIRS failure to the absence of a latent period.

**25.14.4 — Profile likelihood for rho collapses to degenerate CI**
Severity: Major

The reported profile CI for rho is `min = max = 0.00177`, a numerically degenerate result. This indicates that the profile likelihood grid was too coarse to identify distinct lower and upper bounds, or that the likelihood surface within the grid was flat. The paper describes this as a "narrow" CI without noting the failure. Additionally, the best global-search rho (0.00113) lies outside this CI — a contradiction that warrants investigation rather than a suggestion to run more starting points.

Suggested author action: Report all (rho, profile_loglik) pairs from the profile computation. Increase grid density near rho = 0.00177. Apply the 1.92 log-unit cutoff explicitly and verify that the CI spans at least two grid points. If the profile surface is genuinely flat, acknowledge that rho is weakly identified.

**25.14.5 — No non-mechanistic benchmark comparison**
Severity: Major

ARIMA modeling is conducted in the EDA section (ARIMA(2,0,2) preferred), but its log-likelihood is never compared to the POMP models. Without a benchmark, it is impossible to assess whether the added complexity of the mechanistic models produces a meaningful improvement in fit.

Suggested author action: Report the ARIMA(2,0,2) log-likelihood. Note that ARIMA and POMP likelihoods are on comparable absolute probability scales for the same data and can be compared directly (with appropriate care about how the ARIMA likelihood is computed — check whether the software uses the full or conditional likelihood). Discuss whether the SEIRS model's log-likelihood justifies its additional complexity.

**25.14.6 — SIR reporting rate (rho ≈ 0.99) implausible; not diagnosed**
Severity: Major

The SIR global best fit yields `rho = 0.997`. For lab-confirmed influenza, reporting rates of near 100% are epidemiologically implausible; the literature and the SEIRS results (rho ≈ 0.18%) suggest rates far below 1%. This is a clear sign of SIR model misspecification. The paper notes the issue but does not compute a profile likelihood or constrain rho to a realistic range.

Suggested author action: Compute a profile likelihood for rho in the SIR model. Fix or bound rho to a plausible range (e.g., 0.01–0.20) and assess whether the model can fit at all within that range. This would provide a more principled diagnosis of SIR model failure.

**25.14.7 — SIRS pandemic branch never activated (b parameter unidentified)**
Severity: Major

The SIRS step function switches beta based on `t < 261`, but all 261 data observations have `t < 261`, so `beta = b` is never used. The parameter `b` (and implicitly `delta_a`) is therefore structurally unidentified — it cannot be estimated from the data. This goes unacknowledged in the text.

Suggested author action: Remove the pandemic branch from the SIRS model or confirm whether it was intended for out-of-sample prediction. If `b` is not identified, drop it from the model and the parameter search.

---

## Minor Points

**25.14.m1 — Low pfilter replicates in SIR global search**
The SIR global search uses 5 pfilter replicates per chain for logmeanexp. This is low; 10–20 replicates are more standard for reliable estimates. The SEIRS local search used 20 replicates — the SIR global search should be consistent. Suggested fix: increase to at least 10 replicates.

**25.14.m2 — ARIMA model order ambiguity**
The AIC table is applied to the differenced series (`diff_series`) with `order=c(p,0,q)`, which is equivalent to fitting ARIMA(p,1,q) to the original series. The selected "ARIMA(2,0,2)" is therefore actually ARIMA(2,1,2) applied to the original data. This should be stated explicitly.

**25.14.m3 — ChatGPT citations for methodological decisions**
References 7 and 8 cite ChatGPT for decisions about rw.sd settings and profile likelihood interpretation. These are statistical methodology choices that should be grounded in course materials or published references rather than AI assistants. The paper should clarify what specific advice was adopted and verify it against authoritative sources.

**25.14.m4 — Conclusion log-likelihood value inconsistency**
The conclusion text states the SEIRS best value is "-590.46" but the code output shows -591.71. Reconcile these values.

**25.14.m5 — Figure captions**
Most figures are referenced inline without descriptive captions (axis labels, parameter names). Adding captions that identify what each figure shows would improve readability.

**25.14.m6 — Spectral period vs. model period**
The spectral analysis identifies a dominant period of 54 weeks, but 52 weeks is used for seasonal forcing. The decision is reasonable but the sensitivity of results to this choice is not assessed.
