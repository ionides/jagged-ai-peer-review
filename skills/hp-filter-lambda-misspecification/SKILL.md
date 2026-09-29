---
name: hp-filter-lambda-misspecification
description: Detect cases where a time-series project applies the Hodrick-Prescott filter with a lambda value calibrated for a different sampling frequency than the data (e.g., lambda=100 for daily data instead of quarterly), causing over-smoothing or under-smoothing of the trend and distorting all downstream ARMA model selection and stationarity conclusions — use when reviewing a paper that applies hpfilter() or equivalent and cites a conventional lambda value.
---

# HP Filter Lambda Misspecification Detector

## Purpose

The Hodrick-Prescott (HP) filter separates a time series into trend and cyclical components by minimizing a penalized sum of squares, where the penalty weight lambda controls the smoothness of the extracted trend. The conventional lambda values are calibrated to specific sampling frequencies:

| Sampling frequency | Conventional lambda |
|--------------------|---------------------|
| Annual | 100 |
| Quarterly | 1,600 |
| Monthly | 14,400 |
| Weekly | ~677,000 |
| Daily | ~6,812,500 |

A recurring error is to apply lambda=100 (the annual convention) or lambda=1,600 (the quarterly convention) to weekly or daily data, or to cite a course reference that specifies a value appropriate for macroeconomic data without recognizing that the data frequency differs. With too-small a lambda, the HP filter treats low-frequency variation as "cycle" rather than "trend," leaving substantial trend residuals in the detrended series. ARMA models fitted to this incorrectly detrended series will select higher orders than necessary to capture the residual trend, and stationarity test conclusions may be wrong for the correctly detrended series.

## When to Activate

Use this skill when:
- A time-series paper applies the Hodrick-Prescott filter via `hpfilter()` (mFilter package), `hp_filter()`, or equivalent.
- The paper cites a specific lambda (or `freq`) value.
- The data is sampled at a frequency (e.g., daily or weekly) that differs from the sampling frequency for which the cited lambda was calibrated.

Do not use this skill when:
- The paper applies HP filtering to annual or quarterly macroeconomic data and uses the standard lambda for that frequency.
- The paper explicitly justifies its lambda choice with reference to the data frequency and a frequency-appropriate formula.
- HP filtering is used only as a visualization tool with no downstream modeling consequences.

## Procedure

### 1. Identify the sampling frequency of the data

Read the data description to determine the unit of time between observations (daily, weekly, monthly, quarterly, annual). Note the number of observations per year.

### 2. Identify the lambda value used

Locate the `hpfilter(data, freq = lambda, ...)` or equivalent call. Note the numerical value of lambda (the `freq` argument in the `mFilter` package corresponds to lambda directly).

### 3. Compare the used lambda to the frequency-appropriate value

Apply the Ravn-Uhlig rule: the appropriate lambda scales as the fourth power of the ratio of sampling frequencies relative to quarterly data.

- Annual: lambda = 100 * (1/4)^4 ≈ 100 / 256 ≈ 0.39 (but conventionally rounded to 100 for annual)
- Quarterly: lambda = 1,600 (the standard)
- Monthly: lambda = 1,600 * (3)^4 = 1,600 * 81 ≈ 129,600 (conventionally approximated as 14,400)
- Weekly: lambda = 1,600 * (13)^4 ≈ 677,000
- Daily: lambda = 1,600 * (65)^4 ≈ 27,600,000 (or using 260 trading days/year relative to quarterly: 1,600 * (260/4)^4)

If the lambda used differs by more than a factor of 10 from the frequency-appropriate value, flag the misspecification.

### 4. Assess the consequence for downstream modeling

Determine what the HP-filtered residuals are used for:
- If used as input to ARMA model selection: explain that the residual trend will inflate the selected AR or MA orders, and that the ARMA model is capturing the residual trend rather than the cyclical dynamics of interest.
- If used for stationarity testing: the residual trend from under-penalized HP filtering may cause the ADF test to fail to reject the unit root even though the correctly detrended series is stationary.
- If used for a POMP benchmark comparison: the HP-filtered series is on a different scale and distributional family than the POMP observation model, making log-likelihood comparison invalid regardless of the lambda choice.

### 5. Check whether the lambda choice is acknowledged

Read the paper for any statement that justifies the lambda value with reference to the data frequency. If the paper cites a reference appropriate for a different frequency without acknowledging the mismatch, flag the citation as misleading.

### 6. Report the finding

For each detected instance, report:
- The data sampling frequency.
- The lambda value used and the reference cited for it.
- The frequency-appropriate lambda (with the Ravn-Uhlig rule calculation).
- The consequence for downstream modeling (inflated ARMA order, incorrect stationarity conclusion, invalid benchmark comparison).
- The fix: replace the lambda with the frequency-appropriate value, re-run the HP filter, and re-run all downstream analyses (ARMA selection, stationarity tests).

## Limitations

- The Ravn-Uhlig rule gives an approximation; the exact lambda should be chosen based on the desired smoothing properties for the specific application, not mechanically from the rule. If the paper discusses its lambda choice substantively (e.g., calibrating to a specific cycle length of interest), the Ravn-Uhlig rule comparison may not be the right benchmark.
- For non-macroeconomic applications (e.g., epidemiology, finance), the HP filter itself may not be the appropriate detrending method regardless of lambda. The misspecification of lambda is a secondary concern if the method choice itself is questionable.
- Cannot detect the error from the rendered HTML output alone if the lambda value is not stated in the text; source code inspection is required.
- Does not replace the full detrending and stationarity methodology audit; this skill focuses specifically on the lambda calibration failure mode.
