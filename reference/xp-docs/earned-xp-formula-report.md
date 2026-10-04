# Earned XP: whole-data fit and a compact approximation

Research date: October 4, 2026. This report concerns **earned XP relative to observed base XP**. The separate [base-XP report](base-xp-formula-report.md) estimates task workload; performance bonuses and penalties were not used to fit that base.

**Accepted Course Academy rules (version one):** four small, task-specific rules using unweighted question accuracy, a review-ending condition, and provisional low-score penalty bands. This matches **168/168 activities with known base and question outcomes**. It also predicts the confirmed −1 review whose base is unavailable, outside those metrics. The perfect fit describes the saved sample, not a recovered Math Academy algorithm.

The user preferred simple round numbers and approximate symmetry, rather than requiring exact symmetry. We compared symmetric models, freely fitted bands, and compact formulas. The compact choice achieves the same whole-data agreement as a larger band table. Difficulty weighting does not improve that agreement. The penalty thresholds remain weakly supported local defaults.

## Evidence and coverage

The frozen snapshot is dated `2026-10-04T22:04:16.922420+00:00`: **168 activities, 1,634 question occurrences**.

| Type | Activities | Exact selected predictions |
|---|---:|---:|
| Lesson | 80 | 80 |
| Review | 60 | 60 |
| Quiz / assessment | 17 | 17 |
| Multistep | 11 | 11 |
| Total | **168** | **168** |

Sources were merged by task ID, checking overlapping awards, bases, question order, correctness, and difficulty. Overlapping records do not count as separate observations.

| Retained source | Newly represented activities |
|---|---:|
| Completed question captures | 106 |
| Original question-level XP observations | 29 |
| Compact difficulty/outcome observations, joined to progress CSV | 31 |
| Additional live-history observations | 2 |

Source files include [progress.csv](../progress.csv), [original observations](../mathacademy-xp-observations.json), [compact outcomes](../question-difficulty-observations-2026-10-03.json), [live observations](../fire-live-observations-2026-09-26.json), and completed activity states and metadata under `reference/mathacademy/question-capture/`.

**Missing outcomes are not evidence of recording only wrong answers.** The progress CSV contains activity awards and base XP, but no question accuracy. The other sources contain correct, wrong, and perfect activities. We now have complete outcomes for **61 of the CSV's 219 rows**; **158 remain without question outcomes**. The earlier 29-row coverage reflected which historical question records had been included. Another 107 outcome-bearing activities are outside this historical CSV.

All 219 CSV rows were inspected. Missing outcomes were left missing: an award cannot be used to invent accuracy and then count that inferred accuracy as an independent successful prediction. Diagnostics use a different scoring setup and have no usable base-relative formula here. Review `13929099` lacks a recovered base; its separately confirmed negative award is discussed below.

As requested, fitting used all qualifying observations together: **no holdout or separate test set**. No live activities were performed for this investigation. The research did not change captures, the progress CSV, or learner facts. The accepted rules were subsequently integrated into engine scoring as documented below.

## Definitions and rounding

- `B`: observed base XP, the displayed task denominator.
- `C`, `N`: correct and total question occurrences; `p = C/N`.
- `R(x) = floor(x + 0.5)`: nearest-integer rounding, with half ties upward.
- Each question counts once, regardless of answer-field count.
- Quizzes count all assigned questions, including unanswered questions at expiry.

Whole-task accuracy is used, rather than averaging per-knowledge-point percentages. Difficulty multipliers are **E/M/H = 1/1/1** in the selected earned-XP approximation. Task type and base are required; accuracy alone does not determine an award across different task types.

## Selected compact rules

The following are the accepted local engine rules. The 50% and 20% penalty thresholds and −1 floor are our selected defaults.

### Lessons

```text
if p < 0.50:
    XP = -1
elif p == 1:
    XP = R(1.25 × B)
else:
    XP = R(B × min(1, 1.5 × p - 0.30))
```

At 60% accuracy, the multiplier is 0.60. Every one of the 58 captured lessons matches `R(0.60B)`, across bases from 7 to 25. At 75%, it is 0.825; at sufficiently high imperfect accuracy it plateaus at full base. Perfect accuracy receives the separate 25% bonus.

The original line `1.4p − 0.24` also fits every nonnegative lesson. Both belong to a feasible slope interval; **1.5** was selected because it is a simpler half-step coefficient. The raw plateau begins at `p = 13/15 ≈ 86.7%`, but the exact internal cutoff is not established by rounded observations.

The only base-known negative lesson is at 25% accuracy; the lowest nonnegative lesson accuracy observed is 60%. Any low-score cutoff strictly above 25% and at or below 60% gives the same split in this sample. **50% is a convenient round choice within that gap**, not a threshold inferred precisely from the data. Ordinary low-performing lessons can also receive zero according to the public explanation, so this band could overpredict penalties on other tasks.

### Reviews

```text
if p < 0.50:
    XP = -1
elif p == 1:
    XP = B + 2
elif p >= 2/3:
    XP = B
elif the final question is incorrect:
    XP = 0
else:
    XP = R(B × p)
```

The negative review at 40% and positive reviews at 60% support a possible low-score split, with no evidence locating it inside that gap. The 50% default is deliberately shared with lessons for simplicity.

A deterministic formula using only type, base, correct count, and total cannot reproduce these two records:

| Task | Base | Correct / total | Ordered outcomes | Award |
|---|---:|---:|---|---:|
| 13409092 | 6 | 3/5 | `CCICI` | 0 |
| 13938605 | 6 | 3/5 | `CICIC` | 4 |

`C` means correct and `I` incorrect. The final-answer condition distinguishes them, but only **one** retained review supports the terminal-error zero case. It may be a proxy for unsuccessful termination, objective completion, or other hidden state. It is not proof that the last response directly changes XP.

Two consecutive errors do not explain the zero: `CCICI` has none, while task `12698374` has `CCIIC` and earns 2/4 XP. Easy-question mistakes are also insufficient: the zero-award review answers both its easy questions correctly, while all-easy task `13930486` misses two and earns 2/4 XP.

### Quizzes / assessments

```text
if p < 0.20:
    XP = -1
else:
    XP = max(0, R(1.2 × B × (p - 0.35) / 0.65))
```

The ordinary curve connects zero raw reward at 35% accuracy with 120% of base at perfect accuracy. It fits every nonnegative quiz. The 35% intercept is a convenient fitted anchor, not a published threshold.

The negative case has **no submitted answers**; the lowest known nonnegative quiz has 25% accuracy. Any penalty threshold above zero and at or below 25% separates them. The **20% default** is round and compatible, but expiry or nonparticipation could explain the negative award better than accuracy. The sample contains no answered-but-wrong 0% quiz to distinguish those explanations.

### Multistep tasks

```text
XP = max(-1, R(B × (2.25 × p - 1)))
```

This fits all eleven multisteps. Perfect accuracy gives 125% of base. The lowest observed accuracy is 5/9, so negative multistep predictions and the −1 floor are unverified extrapolations. This is a progressive signed line, but there is insufficient evidence to impose the same curve on other task types.

## Why not a single symmetric band table?

We fitted monotone bands to all observations, comparing 60 E/M/H weight pairs per task type. The search used 1% coefficient steps, with a 0.1% strength refinement of the best mirrored candidate. Each fit minimized total absolute integer XP error, then squared error, then band changes. These are comparisons within the explored model families, not a proof of the globally simplest possible formula.

The two symmetric families were:

1. **Equal/opposite total awards:** `XP_raw(p) = -XP_raw(1-p)`, with zero at 50% and endpoints `±(B + perfect bonus)`.
2. **Mirrored endpoint bonus/penalty:** raw endpoints `B + bonus` and `-bonus`, centered at `B/2`, so paired rounded predictions sum to `B` apart from the unavoidable odd-base midpoint.

Both were compared with and without a −1 penalty floor. That floor breaks symmetry after the raw computation. Every band comparison includes the same exploratory review-ending override at 50% through below two-thirds accuracy.

| Candidate | Exact / 168 | Total absolute error |
|---|---:|---:|
| Selected compact rules with provisional penalty bands | **168** | **0 XP** |
| Free accuracy bands, equal difficulty weights, −1 floor | **168** | **0 XP** |
| Free accuracy bands, fitted difficulty weights, −1 floor | **168** | **0 XP** |
| Earlier compact formulas plus review ending, without penalty bands | 166 | 4 XP |
| Mirrored bonus endpoints, fitted weights, −1 floor | 166 | 4 XP |
| Equal/opposite total awards, fitted weights, −1 floor | 164 | 5 XP |
| Free accuracy bands, fixed 1/2/4 weights, −1 floor | 155 | 24 XP |
| Mirrored bonus endpoints, fixed 1/2/4 weights, −1 floor | 151 | 31 XP |

The refined mirrored model still misses the negative lesson by 1 XP and quiz `4833336` by 3 XP. Its fitted weights differ by activity type and its thresholds are irregular fractions. That is more machinery than the compact rules, without improving agreement.

The free equal-weight band fit uses 6 lesson, 4 review, 9 quiz, and 6 multistep levels, including forced endpoints. Several multipliers are awkward, such as 77%, 84%, 57%, and 97%. These are grid-fit values in integer-rounding intervals, not inferred intentional constants. Compact lines capture the same observations with fewer manually stored thresholds.

**Symmetry is useful as a preference when otherwise comparable rules fit similarly. Here, enforcing it reduces agreement and adds complexity.** Perfect bonuses remain simple round amounts, while penalties are treated separately. The evidence does not support extending the 25% reward bonus into an equally sized observed negative penalty.

## What the CSV adds

All above-base CSV awards agree with the proposed ceilings:

| Type | CSV rows | Above-base awards | Proposed ceiling | Matching above-base awards |
|---|---:|---:|---|---:|
| Lesson | 135 | 89 | `R(1.25B)` | 89 |
| Review | 53 | 38 | `B + 2` | 38 |
| Assessment | 13 | 4 | `R(1.20B)` | 4 |
| Multistep | 10 | 5 | `R(1.25B)` | 5 |

The remaining eight CSV rows are diagnostics. Ceiling matches do not establish that every above-base activity was perfect, because many lack outcomes. They do provide independent evidence about the scale of bonuses across task bases.

A single percentage review bonus cannot reproduce all those awards over the observed base range; the additive `+2` is the cheaper fit. Lesson and assessment bonuses consistently support approximately 25% and 20%, respectively, subject to integer-rounding intervals.

The CSV has **no below-−1 examples**. It cannot calibrate the proposed −4 band, an uncapped negative curve, or a penalty escalation schedule. Awards without outcomes constrain ceilings and attainable XP levels, but cannot identify accuracy thresholds.

## Negative awards and hidden state

| Task | Activity | Base | Accuracy / outcome | Award |
|---|---|---:|---|---:|
| 12601433 | Left and Right Riemann Sums in Sigma Notation | 14 | 1/4, `IICI` | −1 |
| 13929099 | The Argument of a Complex Number, review | Unknown | 2/5, `CICII` | −1 |
| 13933898 | Quiz 7 | 15 | 0/9; all unanswered, expired | −1 |

The lesson's difficulty sequence is M/H/E/M; only the easy question is correct. Its displayed times total **20m48s**, with each wrong response taking at least 166 seconds. That is not an obvious rapid-guessing pattern, although times may include pauses.

The review contains five easy questions and takes 77 displayed seconds in total. Its award is confirmed in the [following queue snapshot](../mathacademy/question-capture/13929417/queue-after.json); outcomes are retained in [activity metadata](../mathacademy/question-capture/13929099/activity-metadata.json). Its base is unavailable, so it is excluded from the 168 base-relative cases. The selected low-score rule predicts −1 independently of base.

Quiz 7 followed an [assessment layout error](../mathacademy/question-capture/13933898/diagnostics/1791114247741724783/error.json) and navigation timeouts. Its [saved state](../mathacademy/question-capture/13933898/state.json) records expiry with all nine questions unanswered. That supports a nonparticipation or abandonment explanation as well as a low-accuracy explanation.

Math Academy distinguishes ordinary struggle leading to zero XP from detected rushing or guessing leading to negative XP. Its public FAQ does not say aggregate accuracy is the sole scoring input. [Math Academy FAQ](https://mathacademy.com/faq)

A staff discussion also describes introductory penalty caps and escalation, while qualifying the specific numerical schedule as a recollection. Account history could therefore cause identical task-local performance to earn different penalties. The three −1 examples are compatible with a cap; they do not prove one. Historical zero awards cannot simply be counted as prior capped penalties. [Math Academy Podcast #2, 48:55](https://www.justinmath.com/math-academy-podcast-2/)

The book depicts qualitative reward bands and a jump at passing, without numerical cutoffs. That supports simple bands as a plausible design, but does not establish symmetry or any particular equation. [The Math Academy Way, chapter 22](https://www.justinmath.com/files/the-math-academy-way.pdf#page=312)

To distinguish the negative causes, the most useful additional saved evidence is low-accuracy **zero-award** outcomes, actual submitted versus unanswered counts, task termination/expiry wording, active response times, and chronological penalty history. In particular, recover outcomes for historical zero tasks `4866773`, `11637108`, and `12225753` if available. No deliberate remote failures are required for the present approximation.

## Difficulty weights: where to use them

Difficulty weighting can remain useful when estimating **base workload**. It is not automatically appropriate for earned-XP accuracy. The 1/2/4 workload multipliers and the selection distributions in `schema/engine/2-question-weights.edn` describe different things: estimated cost versus how often each difficulty is asked.

Even after refitting flexible monotone bands, fixed 1/2/4 earned-accuracy weights reproduce only 155/168 awards. Allowing weights to be fitted achieves an exact free-band fit, but the winning weights are simply **1/1/1 for every type**. We therefore retain difficulty in the base-XP calculation, and use ordinary accuracy in the performance adjustment.

This does not rule out every possible hidden difficulty-dependent scoring mechanism. It says that difficulty weighting is unnecessary for the saved awards and makes the proposed straightforward model worse.

## Engine integration

These rules are now the default local scoring policy. [3-xp-weights.edn](../../schema/engine/3-xp-weights.edn) installs version-one rule identities and their formula documentation. It documents fixed coefficients; it does not introduce runtime-tunable XP settings.

The production implementation is `activities::earned_xp` in [activities.rs](../../engine/rust/activities.rs). The four existing activity calculators delegate to it. Runtime completion automatically calculates all four supported activity types when base XP is available. The `use_fitted_xp` switch defaults to true; explicitly disabling it suppresses partial automatic awards in the activity-specific runtime.

The Rust study app's `learning::continuation` and `learning::lesson_xp` use the shared lesson calculation, replacing the previous per-KP mistake-count formula. They award completed failed lessons according to accuracy, independently of the lesson's pass/fail or mastery outcome. Unfinished lessons have no final award. Tutorials and canonical examples are excluded from question counts.

Assessment completion at the time limit and explicit expiry use the full assigned question count for XP. Unanswered questions do not become recorded incorrect answers, submitted responses, or additional FIRe evidence. Explicit caller-supplied observed/imported XP remains authoritative; existing stored awards are not recalculated. Diagnostics retain their separate policy. Base XP continues to be supplied by the caller; this integration changes the earned/base adjustment, not base-workload estimation.

Rust regression checks exercise all 168 saved awards, boundary rounding, partial/failing task completion, generic study-player continuation, and quiz expiry. These are implementation checks of the selected rules, not a held-out research dataset. A focused native EDB check successfully installed all four new documentation identities. The broader `tests/check_rust_edb.sh` harness currently fails before reaching XP because it attempts to install `schema/data/1-2-course-groups.edn` as schema before its referenced attributes exist; this is an existing seed/schema ordering issue. Validation completed with 74 Rust engine tests and 17 passing study-app bridge tests (the live-writer integration test remained ignored).

## Practical use, limits, and reproduction

The [compact estimator](../mathacademy-earned-xp/compact_estimator.py) uses exact integer arithmetic and no external dependencies. A representative lesson call takes about **0.74 microseconds locally**; this is a rough implementation measurement, not an engine benchmark.

```python
estimate_earned_xp("lesson", base=15, correct=9, total=15)  # 9
estimate_earned_xp("assessment", base=15, correct=7, total=10)  # 10
estimate_earned_xp("review", base=6, correct=3, total=5,
                   final_correct=False)  # 0
```

For partial-credit reviews, provide the final outcome; the implementation raises if it is missing rather than inventing state. The formulas reject diagnostic types. The prototype preserves the fitted reference calculation. Production scoring uses the shared engine implementation described below.

**Coverage limits:** 100 of the 168 activities have 60% accuracy, including the deliberate 58-lesson and 40-review capture policies. Most of the curve's shape is supported by a much smaller historical sample. The penalty bands fit only two base-known negative examples and one base-unknown review. Different coefficients and many threshold positions also fit. Mixing older and newer activities assumes scoring policy is reasonably comparable across dates. Using estimated rather than observed base XP adds the separate base model's error.

For a faithful Math Academy prediction, the penalty eligibility and cap should ultimately be separate inputs when recoverable. For a cheap local approximation, the documented defaults give a small, understandable rule set that fits all presently usable awards. Observed and predicted XP should remain separate values.

Artifacts:

- [Frozen evidence](../mathacademy-earned-xp/observations.json): merged outcomes, all CSV rows, source hashes, and exclusions.
- [Selected whole-data results](../mathacademy-earned-xp/compact-results.json): every selected prediction and explicit provisional penalty choices.
- [Compact reproduction](../mathacademy-earned-xp/compact_analysis.py): evaluates the selected rules against all frozen observations.
- [Band comparison results](../mathacademy-earned-xp/band-results.json) and [fitter](../mathacademy-earned-xp/band_fit.py): symmetric/free-band fits, weights, thresholds, and mismatches.
- [Earlier estimator](../mathacademy-earned-xp/estimator.py), [results](../mathacademy-earned-xp/results.json), and [sequence analysis](../mathacademy-earned-xp/sequence-results.json): preserve the non-penalty baseline and difficulty/order comparisons.

Reproduce the selected whole-data fit without refreshing the live capture sources:

```bash
python reference/mathacademy-earned-xp/compact_analysis.py
```

Reproduce the band search with NumPy available:

```bash
/home/jake/Developer/MA/.venv/bin/python reference/mathacademy-earned-xp/band_fit.py
```

`analyze.py --refresh` deliberately replaces the frozen evidence from current saved sources. It is not needed to reproduce this report. Source captures, the CSV, and learner facts remain unchanged.
