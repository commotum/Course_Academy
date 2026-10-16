# Initial frequency weights at the selected fractions

These are the selected initial encompassing estimates. They use the original frequency method and the requested human-friendly fractions.

`w = nearest_fraction(K / N)`

- `K`: original eligible activities with an upward target-band change.
- `N`: all original eligible activities for the same source, target, and account; flats and falls remain in the denominator.
- Allowed weights: **1/5, 1/4, 1/3, 2/5, 1/2, 3/5, 2/3, 3/4, 4/5, 1**.
- Distances are calculated as exact rational numbers; midpoint ties round upward.
- A 1→6 rise contributes one rising activity, as does 3→4. The original jump sizes and full sequences remain available.
- No additional eligibility filters, sample-count threshold, or spacing, magnitude, content, or diagnostic corrections are applied.
- Accounts remain separate. This directory does not select between accounts for a shared database relationship.

There are **1,789 account-specific relationships**, covering **1,730 unique source-target pairs** and **533 source topics**. **651** relationships have one eligible observation and are retained.

| Account | Relationships | Single-observation relationships |
|---|---:|---:|
| foundations | 936 | 272 |
| linear | 274 | 84 |
| multivariable | 372 | 141 |
| differential | 207 | 154 |

| Weight | Account-specific relationships |
|---|---:|
| 1/5 | 6 |
| 1/4 | 56 |
| 1/3 | 316 |
| 2/5 | 1 |
| 1/2 | 637 |
| 3/5 | 1 |
| 2/3 | 30 |
| 3/4 | 2 |
| 4/5 | 0 |
| 1 | 740 |

The original frequency files are preserved unchanged. Each derivative records its original file SHA-256 and retains the underlying source-report path and SHA-256. The numerical `proposed_starting_coverage_weight` is accompanied by exact `weight_fraction` and `frequency_fraction` strings. Values below 1/5 round to 1/5; no zero edge is introduced.

Reproduce from the repository root:

```bash
PYTHONPATH=capture python3 -m scripts.round_encompassing_frequency reference/mathacademy/encompassing-analysis-2026-10-11
```

No database writes are performed by this generator.
