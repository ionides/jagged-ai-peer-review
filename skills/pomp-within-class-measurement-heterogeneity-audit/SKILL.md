---
name: pomp-within-class-measurement-heterogeneity-audit
description: Use when reviewing a pomp project that compares log-likelihoods across two or more POMP model variants (e.g., SIR vs. SEIR vs. SEIQR) where the models may use different dmeas specifications (e.g., one model uses a binomial accumulator, another uses a Gaussian over a stock variable), to detect invalid within-class likelihood comparisons caused by incompatible observation models.
---

# pomp Within-Class Measurement Heterogeneity Audit

## Purpose

In multi-model POMP projects, students frequently extend a working base model (e.g., SIR with a binomial accumulator) to a richer model (e.g., SEIQR) by adding new compartments and modifying the measurement model. When the extended model's measurement model changes in a substantive way — for example, switching from a binomial draw over an accumulator variable to a Gaussian draw over a stock variable — the resulting log-likelihoods are not on a comparable scale, even though both are computed via `pfilter` and reported by `logmeanexp`. A direct numerical comparison and model ranking using these likelihoods is invalid.

This error is distinct from the cross-class comparison error (ARMA vs. GARCH vs. POMP) addressed by `pomp-cross-model-likelihood-audit`. Here, all models are fit as POMP models using the same `mif2` + `pfilter` workflow, so the incompatibility is not obvious from the model labels.

## When to Activate

Use this skill when:
- A POMP project fits two or more compartmental model variants (e.g., SIR, SEIR, SEIQR, SEIRV).
- The project compares log-likelihoods or ranks models based on those comparisons.
- The dmeas Csnippets across the model variants differ in observation distribution family (e.g., binomial vs. Gaussian vs. negative binomial) or differ in the state variable used as the measurement mean/size (e.g., one uses an accumulator H, another uses a stock compartment Q or I).

Do not use this skill when all models under comparison use the same dmeas family with the same observation variable type (e.g., all use negative binomial with an accumulator). In that case, within-class log-likelihood comparisons are valid.

## Procedure

### 1. Enumerate all models and their dmeas specifications

For each model variant, read the dmeas Csnippet and record:
- The distribution family (binomial, negative binomial, Gaussian, Poisson, etc.).
- The state variable used as the mean/size argument (accumulator H, stock compartment I/Q/etc., or a function thereof).
- Whether the state variable is registered in `accumvars` (meaning it is reset at each observation interval) or is a persistent stock.

### 2. Check for distributional family heterogeneity

Compare the distribution families across models:
- If any two models use different distribution families (e.g., binomial vs. Gaussian), flag the comparison as potentially invalid.
- Different families have different natural scales for log-likelihoods: a Gaussian log-likelihood for integer count data will typically be much less negative than a binomial log-likelihood for the same data, because the Gaussian assigns probability mass over a continuous range whereas the binomial is evaluated at the exact observed integer. A model that looks dramatically better by log-likelihood may simply be using a more permissive measurement model.

### 3. Check for stock-vs-accumulator heterogeneity

Compare the observation variable type across models:
- If one model's dmeas observes an accumulator (reset each interval, tracks flow), and another observes a stock (persistent compartment tracking current occupancy), flag the comparison as invalid.
- Observing a stock conflates an individual's contribution across multiple time steps (an individual in quarantine for 7 days contributes to Q on each of those 7 days, but is only a "new case" once). The log-likelihood from a stock-observing model is not interpretable as evidence for incidence data.
- The tell-tale sign: the stock-observing model produces a log-likelihood that is dramatically better (less negative, or higher) than the accumulator-observing models by orders of magnitude.

### 4. Verify that the observation variable matches the data type

For each model, confirm that the observation variable (H, Q, I, etc.) corresponds to what the data actually measure:
- If the data are daily incidence (new confirmed cases per day), the observation variable must be an accumulator of the relevant flow (e.g., H += dN_EI), not a stock.
- If the data are prevalence (current active cases), a stock variable is appropriate.

### 5. Characterize the impact on the model comparison conclusion

If measurement model heterogeneity is found:
- State that the log-likelihood values cannot be directly compared across models.
- Identify which models are on a compatible scale (if any).
- Propose a fix: harmonize the measurement models (same distribution family, same observation variable type) before comparing.
- Note that the model with the anomalously high log-likelihood may appear best not because it captures the data's dynamics better, but because its measurement model is more permissive or misaligned with the data type.

### 6. Summarize findings

For each heterogeneous comparison found:
- Quote the relevant dmeas Csnippets.
- State specifically what differs (distribution family, observation variable type).
- Explain why the log-likelihoods are not comparable.
- Propose the correction.

## Limitations

- This skill addresses measurement model comparability only. It does not evaluate whether any individual measurement model is correctly specified for the data (that is covered by `pomp-seir-accumulator-convention` and `pomp-csnippet-audit`).
- When all models use the same distribution family but differ in parameterization (e.g., different rho values), the likelihoods remain comparable as long as the observation variable type is consistent.
- This skill does not evaluate convergence quality or whether the reported likelihoods represent true MLEs; those are addressed by `pomp-if2-hyperparameter-audit` and the computational adequacy checks in `guided-pomp-review`.
