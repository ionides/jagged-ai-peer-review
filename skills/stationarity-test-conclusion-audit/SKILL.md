---
name: stationarity-test-conclusion-audit
description: Detect inverted or misidentified null-hypothesis conclusions in unit-root and stationarity tests (ADF, KPSS, PP) within time-series papers — use when a project reports an ADF, KPSS, or Phillips-Perron test result and states a conclusion about stationarity.
---

# Stationarity Test Conclusion Audit

## Purpose

Unit-root and stationarity tests have asymmetric null hypotheses that are frequently confused in student and practitioner papers:

- **ADF (Augmented Dickey-Fuller)** and **Phillips-Perron (PP)**: null hypothesis is a unit root (non-stationary); rejecting the null provides evidence *for* stationarity.
- **KPSS (Kwiatkowski-Phillips-Schmidt-Shin)**: null hypothesis is stationarity; rejecting the null provides evidence *against* stationarity.

A recurring error is to state "we retain the null hypothesis of stationarity" after reporting a small ADF p-value (which actually rejects the unit-root null, confirming stationarity), or conversely to interpret a small KPSS p-value as confirming stationarity. These misstatements do not affect the substantive conclusion if the test statistic is read correctly, but they demonstrate a misunderstanding of the hypothesis testing framework and can mislead readers about what was actually tested.

## When to Activate

Use this skill when:
- A time-series paper reports the result of an ADF, KPSS, or Phillips-Perron test.
- The paper states a conclusion about whether the series is stationary or has a unit root.
- The stated conclusion should be cross-checked against the actual null hypothesis of the test used.

Do not use this skill when:
- No unit-root or stationarity test is reported.
- The paper correctly identifies the null hypothesis and states the direction of rejection or retention accurately.
- The test result is reported numerically without any prose conclusion (i.e., no claim is made about the implication).

## Procedure

### 1. Identify the test used

Determine which test is reported: ADF, Phillips-Perron, KPSS, or another variant. Note the function call (e.g., `adf.test()`, `kpss.test()`, `pp.test()` in R).

### 2. Recall the null hypothesis for the test

- `adf.test()` (tseries package): H₀ = unit root present (non-stationary).
- `pp.test()` (tseries package): H₀ = unit root present (non-stationary).
- `kpss.test()` (tseries package): H₀ = series is stationary (level or trend stationary depending on `null` argument).

### 3. Check the stated conclusion against the p-value and null hypothesis

Apply the following logic:

| Test | Small p-value (< α) means | Large p-value (> α) means |
|------|--------------------------|--------------------------|
| ADF / PP | Reject unit root → evidence for stationarity | Fail to reject unit root → insufficient evidence for stationarity |
| KPSS | Reject stationarity → evidence for unit root | Fail to reject stationarity → evidence consistent with stationarity |

Flag any statement that:
- Claims "we keep the null of stationarity" after a small ADF p-value (this conflates the null with the alternative).
- Claims "we reject stationarity" after a large KPSS p-value.
- States "the test confirms stationarity" without acknowledging that ADF/PP only provide evidence against a unit root, not direct proof of stationarity.

### 4. Check whether ADF and KPSS are used together for corroboration

Best practice is to use ADF (or PP) and KPSS together: if ADF rejects the unit-root null and KPSS fails to reject the stationarity null, there is corroborating evidence for stationarity. If a paper uses only one test, note this as a minor limitation.

### 5. Report the finding

For each detected error:
- Quote the specific sentence in the paper that states the incorrect conclusion.
- State the correct interpretation given the p-value and the actual null hypothesis of the test.
- Note whether the substantive conclusion (stationarity or non-stationarity of the series) is affected, or whether only the reasoning is incorrect.

## Limitations

- This skill addresses only the prose conclusion, not the validity of the test itself (e.g., whether the lag length in ADF is appropriately selected, or whether the KPSS bandwidth is reasonable).
- Does not evaluate whether the appropriate test was chosen for the data type (e.g., ADF with trend vs. without trend).
- Cannot detect cases where the test is correct but the series is actually non-stationary and the conclusion is wrong on substantive grounds — it only checks internal consistency between the reported p-value, the test's null hypothesis, and the stated conclusion.
