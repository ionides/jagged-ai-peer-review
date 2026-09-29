## Doug

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Outlier removal without formal justification — no quantitative criterion, analysis not shown robust to inclusion")
- Human Issue #2: covered (matched by finding: "Local search cooling fraction very aggressive — non-converged chains visible in trace plots")
- Human Issue #3: covered (matched by finding: "No non-mechanistic benchmark comparison — no ARIMA/SARIMA/auto-regressive baseline provided")

**Findings classification:**
- Finding 1 (Population conservation violated in R compartment): A — R = pop - S - E - I + vac double-counts vaccinated individuals, inflating population at every step
- Finding 2 (Global search box severely misaligned with MLE): A — declared box excludes actual MLE by factor 10–60 in several parameters
- Finding 3 (Global search initialized from previous mif2 result): A — anti-pattern: mf1 passed instead of base pomp object, cooling schedule near-expired at start
- Finding 4 (Global search performs worse than local by 77 LL units): A — gap of 77.4 log-likelihood units renders global "best parameters" unreliable
- Finding 5 (Negative iota / potential NaN in force of infection): A — iota=-0.43 with non-integer alpha causes pow(negative, non-integer)=NaN in C
- Finding 6 (No non-mechanistic benchmark comparison): B — no ARIMA/SARIMA/auto-regressive baseline (matches Human Issue #3)
- Finding 7 (No profile likelihoods computed): A — no genuine profile likelihoods for any of the 11 estimated parameters
- Finding 8 (Implausible parameter estimates not interrogated): A — R0=82.7 is ~8x literature value; sigma implies 3.2-day incubation vs known 10-21 days
- Finding 9 (Seasonality windows copied from UK measles without verification): A — English school-calendar windows applied to Hungarian data without checking Hungarian calendar
- Finding 10 (Initial conditions inconsistent across searches): C — global search fixes S_0/E_0/I_0/R_0 from local result while local search estimates them, making likelihoods non-comparable
- Finding 11 (Outlier removal without formal justification): D — no prespecified quantitative criterion; authors remove six points without robustness check (matches Human Issue #1)
- Finding 12 (Measurement model uses normal approximation to negative binomial): C — pnorm/rnorm used instead of dnbinom_mu/rnbinom, problematic for small counts
- Finding 13 (rho initialized from cases/births ratio): C — incorrect initialization rationale, though rho is subsequently estimated via IF2
- Finding 14 (Local search cooling fraction very aggressive): D — cooling.fraction.50=0.1 leads to near-zero perturbations by final iteration; non-converged chains visible (matches Human Issue #2)
- Finding 15 (Global evaluation table presents biologically incoherent parameters): C — gamma=922 implies 0.4-day recovery, vr=0.62 contradicts stated low-vaccination motivation, no caveats given

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 0 |
| F (Human-AI contradiction) | 0 |
