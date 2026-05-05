---
name: pomp-nbinom-parameterization-audit
description: Use when reviewing a pomp project whose dmeas Csnippet calls dnbinom(reports, H, rho, give_log) and interprets rho as a reporting rate, to detect the silent error where the NB(size=H, prob=rho) parameterization implies mean = H*(1-rho)/rho rather than mean = rho*H, making rho uninterpretable as a detection probability and all downstream parameter estimates biologically invalid.
---

# pomp Negative Binomial Parameterization Audit

## Purpose

In student POMP projects the negative binomial distribution is used as the observation model to allow overdispersion relative to the Poisson. A common silent error occurs when the dmeas Csnippet uses R's base `dnbinom(reports, size, prob)` convention with the SEIR accumulator H as the size parameter and a "reporting rate" rho as the prob parameter. Under this parameterization, the mean number of reports is size*(1-prob)/prob = H*(1-rho)/rho, not rho*H. For small rho (e.g., 0.05), this yields a mean roughly 19 times H, not 5% of H. The model is internally consistent — dmeas and rmeas agree — so no runtime error occurs, and simulated trajectories may look qualitatively reasonable because the optimizer adjusts all other parameters to compensate. However, rho cannot be interpreted as a reporting fraction, and confidence intervals or biological conclusions about rho are invalid.

The standard epidemiological observation model uses `dnbinom_mu(reports, size=k, mu=rho*H, give_log)` where k is a separate overdispersion parameter and rho genuinely scales the expected report count from the latent case count H.

## When to Activate

Use this skill when:
- A pomp project's dmeas Csnippet contains `dnbinom(reports, H, rho, give_log)` where H is an accumulator variable and rho is described as a "reporting rate," "detection probability," or similar.
- The project interprets the estimated value of rho as a fraction of true cases that are reported.
- The project does not include a separate overdispersion parameter (e.g., k or theta) distinct from the reporting rate.

Do not use this skill when the project uses `dnbinom_mu(reports, size=k, mu=rho*H, give_log)` — that is the correct standard form, and this skill does not apply.

## Procedure

### 1. Identify the dmeas distributional family and argument order

Read the dmeas Csnippet. Determine:
- Which distribution is used (Poisson, binomial, negative binomial)?
- If NB: which parameterization variant? `dnbinom(x, size, prob)` vs. `dnbinom_mu(x, size, mu)`?
- Record the argument assigned to each position.

### 2. Compute the implied mean and compare to the intended model

For `dnbinom(reports, H, rho, give_log)`:
- Implied mean: H*(1-rho)/rho.
- Intended mean (if rho is a reporting rate): rho*H.
- Compute the ratio: [H*(1-rho)/rho] / [rho*H] = (1-rho)/rho^2.
- For rho=0.05: ratio = 0.95/0.0025 = 380. The model's implied mean is 380 times the intended mean.

If the ratio is substantially different from 1, flag as a parameterization error.

### 3. Check rmeas for consistency and whether the error is symmetric

Read the rmeas Csnippet. Determine:
- Does it use `rnbinom(H, rho)` (consistent with the misparameterized dmeas) or `rnbinom_mu(rho*H, k)` (correct)?
- If rmeas and dmeas are both misparameterized in the same way, the simulation and likelihood are internally consistent, but the biological interpretation is wrong.
- If rmeas and dmeas are misparameterized differently, this is the dmeas/rmeas mismatch error covered by `pomp-csnippet-audit` and should be escalated there.

### 4. Assess impact on parameter estimates and conclusions

- With the misparameterization, the optimizer will drive rho toward whatever value minimizes the discrepancy between H*(1-rho)/rho and the actual reports. This is a function of both rho and H, which depends on the process model parameters (mu_IR, beta, eta). All estimated parameters are therefore confounded.
- Identify every conclusion in the paper that depends on interpreting rho as a reporting rate. Flag each as unsupported.
- Note that the confidence interval for rho may be computed correctly (using the model's actual likelihood surface) but corresponds to a quantity that is not the reporting rate.

### 5. Propose the corrected measurement model

The standard replacement for the observation model is:
- dmeas: `dnbinom_mu(reports, k, rho*H, give_log)` where k is an overdispersion parameter to be estimated.
- rmeas: `rnbinom_mu(rho*H, k)`.
- Add k to `paramnames` and include it in `rw.sd` for estimation.

If overdispersion is not of primary interest, a simpler model is binomial: `dbinom(reports, H, rho, give_log)` / `rbinom(H, rho)` where rho is a genuine reporting probability. Note that the binomial model may be inadequate for highly overdispersed count data.

## Limitations

- This skill requires knowing the intended interpretation of the NB parameters from the text. If the authors do not claim rho is a reporting rate, the parameterization may be intentional (e.g., a specific mechanistic model of the observation process).
- The skill addresses parameterization errors in the NB observation model only, not errors in the process model or accumulator convention (those are covered by `pomp-csnippet-audit` and `pomp-seir-accumulator-convention`).
- In models where H is very large (e.g., H = total infectious population in a large epidemic), NB(size=H, prob=rho) can produce a distribution that accidentally approximates a reasonable observation model — but this is coincidental and still does not make rho interpretable as a reporting rate.
