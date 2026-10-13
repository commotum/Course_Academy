# Review-threshold model audit

The observed changes are useful proxies for fractional implicit repetitions earned through other topics. The unresolved question is how that accumulated credit maps to display categories and to the engine's memory scale. These are distinct quantities: a rising band can show successful implicit practice without measuring the memory value that triggers a review.

**Recommendation from this experiment: retain 0.5 provisionally.** The new evidence supports target-specific timing of implicit credit, but changing the numerical review threshold alone does not have demonstrated predictive benefit here. This is not a claim that Math Academy uses 0.5. The value remains a local working choice.

## Fresh analysis performed

This audit read the complete `encompassing-report.md`, the calibration-pilot specification and code, the four frozen timing datasets, and the Rust retention calculation. It then performed a new threshold-profile experiment instead of accepting the earlier report's recommendation.

Each account retains its original chronological split: earliest 70% of audited activities for training, later activities for evaluation. Accounts are never pooled. To avoid imputing unknown upstream memory histories, this experiment uses only observations with a captured prior target-practice time. Flat, rising, and decreasing observations remain included.

The response model extends the previous pilot:

```
H(b) = H1 × 2^(b − 1)
discount = clip((1 − 2^(−hours / H(b))) / (1 − threshold), 0, 1)
expected displayed increment = coverage × amplitude × discount
```

Here `b` is the observed starting band. The growth law and equal band spacing are declared approximations for an observation model, not measurements of actual repetitions. Direct reviews fix coverage at 1 and provide a reference response. A uniform fractional starting position converts expected increments into ending-band probabilities; the original pilot's signed residual handles exceptional changes and the top category is censored.

The experiment profiles thresholds 0.2–0.9, half-lives 6–384 hours on a quarter-octave grid, amplitudes 0.1–2 in 0.1 steps plus 2.5/3/4/5, and residual probabilities 0.01/0.05/0.1/0.2/0.4/0.6. Each threshold gets its own training-only half-life/amplitude/residual fit. This tests whether the threshold contributes information independently of those response parameters. It does not fit queue eligibility or a due-state label.

## Direct-practice calibration does not identify a stable threshold

All four early training fits selected the upper grid edge, 0.9. The improvement over 0.5 was less than 1.1 total log-likelihood units in every account; the selected half-life changed substantially to compensate. These descriptive profile differences are not independent-sample confidence intervals.

| Account | Train / later reviews with known age | Improvement in total training log likelihood over 0.5 | Later transition log loss at 0.5 | Later loss at selected 0.9 | Full-data selected threshold |
|---|---:|---:|---:|---:|---:|
| Foundations | 415 / 146 | 0.915 | 0.955 | 0.950 | 0.7 |
| Linear | 163 / 108 | 1.071 | 0.641 | 0.644 | 0.3 |
| Multivariable | 135 / 62 | 0.288 | 0.837 | 0.894 | 0.9 |
| Differential | 105 / 56 | 0.551 | 0.943 | 1.415 | 0.4 |

Lower prediction loss is better. Full-data selections are descriptive refits, not held-out results. In foundations, for example, threshold 0.5 fits a 24-hour response half-life; threshold 0.9 fits 135.8 hours. Their discounts reach full strength at 24 and 20.6 hours respectively. Nearly the same effective response timing can therefore receive very different numerical threshold labels.

Repeating the profile using only starting-band-1 reviews with exactly 60% accuracy retains the same early preference for 0.9 and the same lack of later benefit in three accounts. Using time since any possible prerequisite-based refresh instead selects the shortest permitted response half-life in every account. That clock treats some non-encompassing prerequisite work as a refresh, demonstrating sensitivity to how implicit updates are reconstructed.

## Held-out implicit-credit check

This check uses implicit observations only: work on another source topic with the target appearing as a structural prerequisite. Relationships must have shown a rise in early training, with no minimum activity-count exclusion. Each account's coverage weights are frozen at the original pilot's training-only fitted values. All evaluated activities occur later, and all target observations from one activity stay together. A companion comparison uses training-only frequency weights.

| Account | Later implicit observations / activities | Transition log loss, threshold 0.5 | Loss, direct-reference-selected 0.9 | Crossing Brier, 0.5 → 0.9 |
|---|---:|---:|---:|---:|
| Foundations | 27 / 15 | 1.472 | 1.482 | 0.129 → 0.131 |
| Linear | 7 / 5 | 1.924 | 1.944 | 0.397 → 0.398 |
| Multivariable | 52 / 29 | 1.596 | 1.837 | 0.289 → 0.301 |
| Differential | 4 / 4 | 1.645 | 1.632 | 0.557 → 0.553 |

Changing the threshold fails to improve implicit-credit predictions consistently. The small differential sample gives little guidance. These are conditional sensitivity checks: the original coverage weights were estimated with the earlier 0.5 observation model. Jointly refitting coverage could absorb a changed timing response, which is precisely another source of ambiguity. These scores do not establish that 0.5 is optimal, and they do not imply that implicit practice is absent when a band stays flat.

## Intervening implicit practice changes the interpretation of elapsed time

An additional target-by-target audit finds eligible implicit exposures strictly between each prior direct practice and the later direct review. It distinguishes visible implicit rises from exposures that remain in the same band. These are captured observations, not a complete numerical credit ledger.

| Account | Later direct reviews preceded by an observed implicit rise | Median gap since direct practice, with a rise | Median gap without an observed rise | Median age of last possible implicit/direct practice, with a rise |
|---|---:|---:|---:|---:|
| Foundations | 25 | 26.2 h | 14.4 h | 0.62 h |
| Linear | 10 | 31.1 h | 14.7 h | 0.34 h |
| Multivariable | 8 | 24.3 h | 12.6 h | 0.11 h |
| Differential | 2 | 34.8 h | 14.7 h | 8.72 h |

These descriptive comparisons are consistent with implicit practice postponing direct review. They do not isolate a causal delay: topic mix, initial band, credit size, selection, and unobserved flat-band credit differ. A review after 26 hours is not evidence that memory simply decayed for 26 hours when the target was practiced within the preceding hour.

To test whether the threshold ambiguity merely came from ignoring intervening practice, the profile was also fitted to the conservative subset with **no captured intervening potential prerequisite-based practice**. Training/test counts were 168/55, 49/33, 17/23, and 42/16. Selected thresholds were 0.9, 0.7, 0.9, and 0.9, but their later transition losses differed from threshold 0.5 by only −0.00110, +0.00049, −0.00038, and +0.00290. The time scale and response amplitude again absorb the threshold change. The subset is small in some accounts, and even here missing captures cannot establish a complete history.

This controls part of the problem; it does not replace an operational replay. The proper replay would apply each implicit fractional increment when it happened, update the target's memory and interval, and then predict the next ordinary-review offer. Resetting a clock after every possible descendant activity is not equivalent to that replay. Neither is timing everything from the last explicit review.

## What would identify the operational threshold better?

The Rust engine schedules a review at

```
due age = stored half-life × log2(stored memory / threshold)
```

Even a perfectly observed due age does not determine the threshold unless memory and half-life are independently anchored. Starting at memory 1, a 48-hour review can be produced by threshold 0.5 with a 48-hour half-life, or threshold 0.8 with a 149.1-hour half-life. Implicit practice also changes the memory anchor and interval, so time since the last direct review is not the full state.

Use the band histories to estimate the **relative amount and timing of implicit repetition credit**, while validating the resulting review times against independently observed ordinary-review offers. Fit threshold together with the time scale only after fixing a defensible repetition/display mapping or expressing the fitted result as an effective interval. Keep remedial and optional early-review events separate from ordinary due-review evidence. Learning speed, task quality, band boundaries, and intervening implicit updates cannot all be freely fitted and then presented as a uniquely recovered threshold.

The held-out checks here evaluate color-response predictions. They are not a verdict on how well the current engine reproduces actual ordinary-review offer times; that requires the separate queue/offer audit.

## Artifacts and reproduction

- `threshold-profile.json`: source hashes, account-local split dates, every threshold fit, later scores, and exact included observations.
- `implicit-threshold-check.json`: fixed coverage weights, every later implicit observation, account-local threshold scores, and source hashes.
- `intervening-implicit.json`: per-target intervening exposures/rises, clock strata, and the clean-subset response fits.
- `profile_threshold.py`, `implicit_threshold_check.py`, and `intervening_implicit.py`: the calculations.

From the repository root:

```sh
/home/jake/Developer/MA/.venv/bin/python reference/analysis/review-threshold-2026-10-11/model-audit/profile_threshold.py
/home/jake/Developer/MA/.venv/bin/python reference/analysis/review-threshold-2026-10-11/model-audit/implicit_threshold_check.py
/home/jake/Developer/MA/.venv/bin/python reference/analysis/review-threshold-2026-10-11/model-audit/intervening_implicit.py
```

No engine settings, database facts, captured observations, or existing reports were changed.
