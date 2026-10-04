# Base XP calibrated to all captured lessons

Updated October 4, 2026. The target is **base XP only**, the task's displayed denominator. Earned XP, bonuses, penalties, accuracy, and actual learner/bot time are not inputs or fitting targets.

At Jake's request, the current calculation fits **all 58 completed lessons**, with no held-out set or cross-validation. All coefficient, multiplier, and model choices use those observations. The errors below describe agreement with these captures, not accuracy on unseen content.

## Result

Difficulty multipliers improve this approximation when applied to a content-workload measure. The best searched small multiplier set is:

```text
Easy × 1
Moderate × 2
Hard × 4
```

These multiply the mathematical length of a question's worked solution. They are **not** fixed per-question XP amounts or recovered MA duration ratios. The band is called `moderate` in the schema; it is the middle difficulty band.

Adding other cheap content measurements gives **1.95 XP mean absolute error** across all 58 lessons, down from **2.60 XP** for the initial formula fitted to the same whole dataset. Twenty-five bases match exactly, 43/58 are within 2 XP, and 46/58 within 3 XP. The worst error remains 11 XP.

A compact alternative uses four cached measurements and averages **2.02 XP error**. Numeric evaluation took about **3.4 microseconds** for the fuller formula and **1.0 microsecond** for the compact one in a local benchmark. Both use only Python's standard library at runtime.

## What the schema weights mean

[2-question-weights.edn](../../schema/engine/2-question-weights.edn) defines **selection probabilities**, not time costs. The current configured numbers are in [3-default-fire-policy.edn](../../schema/engine/3-default-fire-policy.edn):

| Activity/phase | Easy | Moderate | Hard |
|---|---:|---:|---:|
| Lesson initial | 60% | 30% | 10% |
| Lesson remedial | 45% | 55% | 0% |
| Review initial | 40% | 40% | 20% |
| Review remedial | 90% | 10% | 0% |

For expected question times tE, tM, and tH, the lesson's initial expected question time would be approximately `0.60tE + 0.30tM + 0.10tH`, before handling unavailable bands. This is how selection weights can help price the work our generator intends to serve. A duration multiplier is a separate input to tE/tM/tH.

The Rust sampler chooses a difficulty band first and renormalizes over eligible bands before selecting a question within the band. It switches after two questions per lesson KP or three per review. These defaults were reconstructed from observations; they are not claimed to be MA's true parameters. [Sampler implementation](../../engine/rust/question_selection.rs).

I compared reweighting captured solution lengths with the policy distributions against applying duration multipliers to the captured difficulty-labelled questions. Selection probabilities by themselves did not improve the rounded mean absolute error beyond the refined unweighted formula. Difficulty-dependent duration did.

## Comparisons on the entire dataset

All rows use the same 58 base-XP observations. The current fitting minimizes rounded absolute XP error, then squared error, while preserving a seven-XP floor and nonnegative workload coefficients.

| Candidate | Mean absolute error | Root mean squared error |
|---|---:|---:|
| Original first-pass formula | 2.60 XP | 3.83 XP |
| Same features, refined around rounding and the floor | 2.34 XP | 3.92 XP |
| KP count and E/M/H shares alone | 3.29 XP | 4.39 XP |
| Policy initial selection weights applied to solution lengths | 2.34 XP | 3.98 XP |
| Policy-weighted lengths with fitted band-specific duration coefficients | 2.22 XP | 3.76 XP |
| Solution-length duration multipliers 1/1.5/2 | 2.14 XP | 3.60 XP |
| Solution-length duration multipliers 1/2/3 | 2.07 XP | 3.46 XP |
| Fitted 1/2/4 multipliers, compact formula with extra fields | 2.02 XP | 3.31 XP |
| **1/2/4 multipliers plus fuller content features** | **1.95 XP** | **3.32 XP** |

The multiplier search fixes Easy at one and searches Moderate from 1 to 4 and Hard from Moderate to 5, in increments of 0.5. Nearby values also fit similarly: 1/1.5/3 yields 2.03 XP error and 1/2.5/5 yields 2.05. There is no reason to interpret 1/2/4 as uniquely identified. These are the best candidates found by the deterministic search, not a guarantee of a global minimum.

The fuller fit gains only about four XP of total absolute-error reduction across all 58 lessons compared with the compact one. Both are saved so we can choose between fewer measurements and the closest aggregate match.

## Measurements and formulas

Average within each KP's captured question pool, then sum those averages across KPs. This prevents the bot's deliberate five-question sequence from inflating the priced workload. Copying equivalent questions into a pool leaves its measurements unchanged.

The main difficulty-weighted measurement is:

```text
W = sum over KPs mean over questions (
      solution math-token count × difficulty multiplier
    )
```

A math token is a LaTeX command, number, individual letter, or arithmetic/equality/script operator inside a Markdown formula. Image paths and blank-field placeholders are excluded. No semantic model or OCR is used.

The compact formula is:

```text
B = max(7, round_half_up(
      0.23717 + 0.32457 K + 0.01200995 W + 0.00079668 R + 2.52045 F
    ))
```

K is KP count; R is tutorial/canonical-example prose words; F is the sum of each KP's mean number of answer fields beyond the first. Full-precision coefficients are stored in [estimator.py](estimator.py).

The fuller formula uses these cached features:

| Feature | Meaning | Fitted coefficient |
|---|---|---:|
| W/100 | Difficulty-weighted solution math tokens | 0.77275065 |
| R/100 | Tutorial and canonical-example prose words | 0.07513005 |
| S | Sum of per-KP mean equals-sign counts in question solutions | 0.00158606 |
| E | Equals signs in canonical-example solutions | 0.03442212 |
| P/100 | Sum of per-KP mean prompt math tokens | 2.73490184 |
| F | Sum of per-KP mean extra answer fields | 0.06047150 |
| A | Sum of per-KP fractions of questions with blank answers | 0.57420341 |
| M | Sum of per-KP fractions of moderate questions | 0.87087352 |
| H | Sum of per-KP fractions of hard questions | 2.04185092 |

Multiply each feature by its coefficient, sum, round half upward once, and apply the seven-XP floor. The fitter gave the separate intercept, KP-count coefficient, and tutorial-count coefficient zero. KP scope is still represented because the other measurements are summed across KPs; this does not imply KPs or tutorials contribute no actual time.

These are predictive coefficients, not literal reading speeds or independent physical timing components. No 25-XP cap is applied. The seven-XP floor is supported by this lesson population: 28/58 captured lessons are exactly 7 XP, and all 135 historical lesson rows have base at least 7. It should not automatically be applied to individual questions, reviews, or arbitrary short activities.

![Fit to all 58 captured lessons](full-fit.png)

## Remaining mismatches

Some intrinsic workload still is not represented by these measurements:

| Topic | Observed base | Fuller fitted base |
|---|---:|---:|
| Describing the Position Vector of a Point Using Known Vectors | 25 | 14 |
| Vertical Asymptotes of Rational Functions | 25 | 15 |
| Calculating the Equation of a Normal Line Using Differentiation | 19 | 10 |
| Differentiating Reciprocal Trigonometric Functions | 22 | 14 |
| Limits at Infinity of Polynomials | 7 | 13 |

Text and math length cannot fully price diagram reasoning, conceptual novelty, or the difficulty of selecting the correct procedure. These discrepancies are discrepancies in **base XP**, not effects of excellent or poor learner performance. Known observed bases should take precedence over a fitted guess.

The selection-probability experiment also has a supply limitation: 136 of 190 captured KP pools have no observed Hard question, 41 no Easy, and 38 no Moderate. Absence from five sampled questions does not establish absence from MA's full bank. Reweighting uses the bands present in the captured pool, matching our local sampler's behavior for that pool. Two KP samples contain only Hard questions and expose no positively weighted remedial band; their exploratory remedial time borrows their initial estimate. No sampling configuration was changed to invent a Hard remedy.

## Data and use

The frozen data are from **2026-10-04 21:16:25 UTC**. I checked for additional completed lesson captures during this revision; there were none. Every one of the 58 complete lesson observations is included in the fit. The dataset also retains 40 known-base reviews, four quizzes, and three complete multisteps; these do not enter the lesson regression.

The initial investigation's factual observations remain useful: three-KP lessons span 7–19 XP, four-KP lessons 7–25; 16/17 lesson topics overlapping historical progress retained exactly the same base; all four captured quiz bases match their 14/15/12/15-minute limits. Expected workload is the natural mechanism described by [Skycak](https://www.justinmath.com/golden-nuggets-podcast-39/). The [initial report](initial-analysis.md) retains that first investigation and its superseded validation procedure.

- [observations.json](observations.json): frozen captures, base evidence, source IDs/hashes, content measurements, and historical observations.
- [results.json](results.json): current all-data fits, multiplier search, coefficients, per-topic predictions, and residuals.
- [observed-bases.json](observed-bases.json): observed bases for 163 lesson topics and 70 review topics, retaining differing older values.
- [estimator.py](estimator.py): current full estimator, compact alternative, content-feature preparation, and the original first-pass formula for comparison. Runtime uses only Python's standard library.

Prepare `features = lesson_features(content, tutorial_prose_word_count)` once, then call `estimate_from_features(features)`. The compact alternative is `estimate_weighted_lesson_base(K, W, R, F)`.

Recompute the calibration with:

```sh
/home/jake/Developer/MA/.venv/bin/python reference/mathacademy-base-xp/analyze.py
```

This now fits all observations without any data split. `--refresh` deliberately replaces the frozen observations with current saved captures. Refreshing or changing the fit can produce new coefficients; the standalone estimator's constants reflect the current recorded fit and should be updated together with a future calibration.

Capture behavior, schema weights, database facts, and learner progress were not changed. The estimator is not yet integrated into scheduling or awards.
