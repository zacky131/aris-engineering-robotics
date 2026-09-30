# Statistical Reporting — Global Rule

Statistical analysis in robotics and control research must meet these standards.

---

## Required reporting for repeated trials

| N | Minimum reporting |
|---|---|
| N = 1 | Raw value only; no aggregate statistics; explicitly state single trial |
| N = 2–4 | Mean and range (min, max); note small N |
| N ≥ 5 | Mean ± std; consider 95% confidence interval |
| N ≥ 10 | Mean ± std + 95% CI; consider Wilcoxon or t-test for comparisons |
| N ≥ 30 | Full descriptive statistics; formal hypothesis test recommended |

Always state N explicitly.

---

## Hypothesis testing rules

Before running a statistical test:
1. State the null hypothesis explicitly.
2. Choose the test before seeing data (pre-registration preferred).
3. Verify assumptions (normality, independence, homoscedasticity).
4. Report: test name, test statistic, p-value, effect size.
5. Do not report p-value alone; always include effect size.

Recommended tests for robotics:
- Two-sample: Wilcoxon rank-sum (non-parametric) or Welch's t-test
- Paired: Wilcoxon signed-rank or paired t-test
- Multiple groups: Kruskal-Wallis + post-hoc

Do not use repeated hypothesis tests without multiple-testing correction.

---

## Significance threshold

Do not claim "statistically significant" without:
- α stated (default: 0.05)
- p-value < α confirmed
- Effect size (Cohen's d or rank-biserial r) reported

---

## Prohibited claims without justification

| Claim | Requires |
|---|---|
| "significantly better" | Formal test + effect size |
| "outperforms" | Statistical comparison with confidence |
| "robust" | Tested across the claimed disturbance range |
| "always converges" | Formal proof or exhaustive empirical demonstration |

---

## Confidence interval reporting

Format: `mean ± CI_half [units], N=n, 95% CI`

Example: `position RMSE: 0.34 ± 0.04 m, N=20, 95% CI`

---

## Random seed policy

Always document one of:
- `fixed_seed: <value>` — same seed for all methods and trials
- `matched_random: <N seeds>` — N random seeds shared across all methods
- `independent_random` — note this prevents direct statistical comparison between runs

Shared seeds are required for fair method comparison.
