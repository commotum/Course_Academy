# Math Academy XP: observed rules and tested hypotheses

Research date: 2026-09-24. The evidence supports a systematic calculation with a calibrated workload baseline and a performance adjustment. It does **not** support a universal fixed number of XP per Easy, Moderate, or Hard question.

Two compact formulas reproduce all inspected Assessment and Multistep awards. Their coefficients are hypotheses fitted to observed integer outputs, not recovered Math Academy code. Lesson and Review bonuses are clearer than their partial-credit rules. Diagnostic and Supplemental Diagnostic scoring remains unresolved.

## Evidence and notation

The analysis uses the 214-row `progress.csv` snapshot and completed-task DOM observations from Chrome: **34 tasks, 308 questions**.

| Type | Inspected tasks | Questions | Coverage |
|---|---:|---:|---|
| Lesson | 5 | 46 | Perfect, partial credit, negative XP; four tasks retain KP group boundaries |
| Review | 6 | 24 | Bonus, full base, half base, zero |
| Assessment | 12 | 110 | Every assessment in the CSV |
| Multistep | 6 | 50 | Every below-ceiling multistep, plus one perfect task |
| Diagnostic | 3 | 70 | Calculus I, Calculus II, Multivariable Calculus |
| Supplemental Diagnostic | 2 | 8 | Both entries in the CSV |

The earlier activity-schema investigation also inspected the 65-question diagnostic 13469233. It is not included in these numerical fits because its question-level observations were not retained in this dataset. Historical links later began redirecting to an active assessment; browsing stopped without answering or submitting anything.

- `B`: displayed XP denominator, stored as `xp-possible` in the existing CSV. Interpret it as **base XP**, not a maximum; bonuses exceed it.
- `Y`: awarded XP.
- `N`: number of displayed question occurrences, including incorrect/no-answer results.
- `C`: correct question occurrences; `p = C/N`.
- `R(x) = floor(x + 1/2)`: nearest integer, ties upward. The implementation below uses exact rational arithmetic.
- Question difficulty is the displayed `E`, `M`, or `H` label. A wrong response displaying `No answer` is retained separately from a wrong submitted answer. This label does not establish why an answer is missing.

Observations contain model features, not full prompts, solutions, or a complete export of the activity schema. Dates come from the CSV; elapsed values come from question-result elements. Elapsed time may include pauses. The earlier schema report documents a date discrepancy for diagnostic 4748206, so its history should not be treated as a clean timing experiment.

## How base XP is assigned

Math Academy's chief quantitative researcher describes lesson XP as an estimate built from knowledge points, tutorial slides, expected question counts, and expected time per question. Content writers estimate timings, and student data later calibrates them. The natural structural hypothesis is therefore:

```text
base XP ≈ calibrated instructional time + calibrated expected question time
```

This is a model of the mechanism, not a published sum or rounding formula. An XP roughly represents an expected minute for a serious average student. It is not the particular learner's stopwatch time. [Skycak, Golden Nuggets Podcast #39](https://www.justinmath.com/golden-nuggets-podcast-39/)

Quizzes also target expected duration rather than a fixed question count; the published explanation contrasts roughly 20 elementary questions with 6–7 calculus questions in a 15-minute quiz. That supports question-specific workload estimates. [Chalk and Talk #42](https://www.justinmath.com/chalk-and-talk-podcast-42/)

Private-data checks:

- `B = #E + 2#M + 3#H` fit the first three inspected quizzes, then failed held-out examples. Task 12324960 has a difficulty sum of 14 but base 13. Task 4866663 has a sum of 15 but base 12.
- Repeated Review topics and Multistep titles retain their bases in the CSV. Two repeated Lesson topics change by one XP across dates; the baseline cannot safely be treated as an immutable topic constant.
- Difficulty labels, actual question count, and elapsed time do not expose the expected-time parameters or original planned workload. In Lessons and Reviews, adaptive questions further separate displayed count from planned count.

## Assessment: a formula fits all 12 observed awards

```text
Ŷ = max(0, R(1.2 × B × (p − 0.35) / 0.65))
```

This is a continuous accuracy-based scale with a 20% perfect-performance bonus and an inferred zero crossing near 35%. Every question has equal weight in `p`, irrespective of its displayed difficulty. No-answer results count as incorrect in this candidate.

| Task | Base B | Correct/N | Actual Y | Predicted |
|---|---:|---:|---:|---:|
| [13553418](https://mathacademy.com/learn?taskId=13553418) | 15 | 7/10 | 10 | 10 |
| [13467292](https://mathacademy.com/learn?taskId=13467292) | 15 | 5/8 | 8 | 8 |
| [13128427](https://mathacademy.com/learn?taskId=13128427) | 15 | 7/9 | 12 | 12 |
| [12721190](https://mathacademy.com/learn?taskId=12721190) | 15 | 10/11 | 15 | 15 |
| [12324960](https://mathacademy.com/learn?taskId=12324960) | 13 | 7/7 | 16 | 16 |
| [12293511](https://mathacademy.com/learn?taskId=12293511) | 15 | 8/8 | 18 | 18 |
| [12228526](https://mathacademy.com/learn?taskId=12228526) | 13 | 7/8 | 13 | 13 |
| [12225370](https://mathacademy.com/learn?taskId=12225370) | 11 | 2/8 | 0 | 0 |
| [6907144](https://mathacademy.com/learn?taskId=6907144) | 15 | 8/12 | 9 | 9 |
| [4866663](https://mathacademy.com/learn?taskId=4866663) | 12 | 11/11 | 14 | 14 |
| [4833693](https://mathacademy.com/learn?taskId=4833693) | 11 | 6/9 | 6 | 6 |
| [4833336](https://mathacademy.com/learn?taskId=4833336) | 12 | 4/9 | 2 | 2 |

For today's Quiz 4: `1.2 × 15 × (0.7 − 0.35)/0.65 = 9.6923…`, which rounds to **10 XP**.

Why 35% is plausible: after fixing the perfect multiplier at 1.2, a rounded straight-line model compatible with the observations has a zero crossing between approximately 34.55% and 35.71%. The simple 35% choice lies inside that interval. All three perfect quizzes match `R(1.2B)`. A universal rounded 25% bonus fails two of them.

**Limits:** this is an in-sample fit after candidate revision, not 12 independent holdout tests. Nearby coefficients and nonlinear curves can also reproduce these integers. No nonzero result below 44.4% accuracy was observed, so the 35% cutoff is inferred, not directly measured. The zero clamp could conceal a history-dependent negative cap. A two-parameter affine model using E=1/M=2/H=3 weighted accuracy cannot fit all 12 awards with either nearest or floor rounding; that particular weighting is worse supported than raw accuracy.

Useful future predictions at base 15: 60% → 7 XP; 75% → 11; 85% → 14; 95% → 17. The last would distinguish this model from one that only awards above-base XP for perfect performance. These predictions can be checked on naturally occurring tasks without intentionally missing answers.

## Multistep: six exact matches, including two later checks

```text
Ŷ = R(B × (2.25p − 1))
   = R(B × (1.25C/N − (N−C)/N))
```

The second expression suggests a 1.25 contribution for correct work and a −1 contribution for incorrect work, scaled by base XP and question count. This is an algebraic interpretation, not evidence that the implementation scores each question separately.

| Task | Base B | Correct/N | Actual Y | Predicted |
|---|---:|---:|---:|---:|
| [13498401](https://mathacademy.com/learn?taskId=13498401) | 10 | 7/7 | 13 | 13 |
| [4834235](https://mathacademy.com/learn?taskId=4834235) | 10 | 5/7 | 6 | 6 |
| [11976594](https://mathacademy.com/learn?taskId=11976594) | 15 | 8/10 | 12 | 12 |
| [4821880](https://mathacademy.com/learn?taskId=4821880) | 7 | 5/9 | 2 | 2 |
| [13129162](https://mathacademy.com/learn?taskId=13129162) | 14 | 7/9 | 11 | 11 |
| [12722018](https://mathacademy.com/learn?taskId=12722018) | 7 | 7/8 | 7 | 7 |

The last two were inspected after selecting this candidate from the first four. The quadratic-profit pair also controls for task content and base: the same seven-question difficulty pattern yields 13/10 when perfect and 6/10 with two mistakes.

**Limits:** the samples do not identify a unique slope. Holding the perfect factor at 1.25 permits slopes above 2.1 through 2.25. The chosen formula gives exactly 10.5 for task 13129162, consistent with its rounded award of 11. No inspected Multistep has accuracy below 5/9; extrapolation to zero or negative XP and any history cap is untested.

## Lesson: bonus supported; partial-credit formula unresolved

The perfect lesson 13512234 earns `20/16 = 1.25`. Across all 133 Lesson rows, **89 awards equal `R(1.25B)` and none exceed it**. Those 89 are ceiling matches; their question-level correctness was not all inspected.

Using the Multistep formula for Lessons fails:

| Task | Correct/N | KP question counts | Actual XP | Multistep formula |
|---|---:|---|---:|---:|
| 13510941 | 8/9 | 2,2,2,3 | 19/19 | 19 |
| 13512234 | 8/8 | 2,2,2,2 | 20/16 | 20 |
| 13497944 | 10/13 | 2,4,3,4 | 8/9 | 7 |
| 13471622 | 9/12 | 2,3,2,5 | 12/15 | 10 |
| 12601433 | 1/4 | Two displayed groups | −1/14 | −6 |

For 13497944, the four KP sequences are `CC`, `CICC`, `ICC`, `CICC`, with C=correct and I=incorrect. Repeated successes after errors inflate the displayed question count. For 13471622 they are `CC`, `ICC`, `CC`, `CICIC`; the final group's stopping state differs. This makes completion/mastery state, question-specific workload, and the adaptive sequence plausible missing inputs. Neither raw accuracy nor mistake count alone has produced a verified rule here.

Math Academy's book describes performance bands, a jump at passing, and larger penalties after repeated poor tasks, rather than publishing an exact equation. That supports testing a piecewise state-dependent model. It does not establish which thresholds apply to each type. [The Math Academy Way, pp. 309–313](https://www.justinmath.com/files/the-math-academy-way.pdf#page=309)

Negative XP may also depend on account history: Skycak tentatively recalls initial penalty caps of 0, then −1, then −2, each for three penalties. This is staff recollection, not a verified current numeric policy. It can explain why a task-local negative formula alone is insufficient; it does not prove the −1 lesson's exact cap. [Math Academy Podcast #2, 48:55](https://www.justinmath.com/math-academy-podcast-2/)

## Review: apparent two-XP perfect bonus, plus adaptive performance state

The inspected perfect review 13124977 earns 9/7. Across all 51 Review rows, **36 awards equal `B+2`, and none exceed it**. The available bases are only 4–7. A minimum-two-point quarter-base bonus, `B + max(2, R(B/4))`, is indistinguishable on that range. A perfect base-10 review would distinguish +2 from the alternative (+3).

| Task | Ordered outcomes (lowercase = incorrect) | Correct/N | XP |
|---|---|---:|---:|
| 13675888 | mEE | 2/3 | 4/4 |
| 13537500 | EEeEE | 4/5 | 4/4 |
| 13129456 | mEM | 2/3 | 6/6 |
| 12698374 | MEeeE | 3/5 | 2/4 |
| 13409092 | EMmEm | 3/5 | 0/6 |
| 13124977 | EHE | 3/3 | 9/7 |

One mistake can still earn the base. Two mistakes can yield half the base or zero at the same 3/5 raw accuracy. A universal multiplier of accuracy cannot explain the last contrast, and `B+2−2×mistakes` fails the zero-XP review. Differences in question difficulty, KP objectives, adaptive selection, and termination are viable explanations; the page's green completed checkmark is not an exposed internal pass/fail score.

Leading structural hypothesis: first determine the adaptive review's performance/completion state, then award the appropriate band and bonus. The transition rule and difficulty weights remain unknown.

## Diagnostic and Supplemental Diagnostic: distinct scoring remains unidentified

Both result-page types omit base XP. Their shared DOM structure does not demonstrate shared scoring.

| Type/task | Correct/N | Incorrect with shown answer | `No answer` | Earned | Sum of displayed elapsed time |
|---|---:|---:|---:|---:|---:|
| Diagnostic 12563189 | 3/16 | 0 | 13 | 2 | 20.60 min |
| Diagnostic 4748206 | 3/9 | 1 | 5 | 0 | 11.90 min |
| Diagnostic 11604423 | 20/45 | 2 | 23 | 31 | 50.25 min |
| Supplemental 9319474 | 2/3 | 0 | 1 | 4 | 2.82 min |
| Supplemental 5454029 | 3/5 | 0 | 2 | 3 | 7.72 min |

What the data establish:

- The quiz model with a 35% cutoff cannot apply unchanged: diagnostic 12563189 earns positive XP at only 18.75% accuracy, regardless of an unknown positive baseline.
- Counting correct questions alone fails: both Supplemental 5454029 and Diagnostic 4748206 have three correct Moderate questions, but earn 3 and 0 XP. This falsifies a shared correct-difficulty-only rule, not every possible type-specific rule.
- Even within Supplementals, three correct Moderate questions earn less than one correct Moderate plus one correct Easy question. Fixed increasing difficulty weights per correct answer do not explain both awards without other terms.
- Actual elapsed minutes alone do not explain the awards.

Candidate mechanisms to investigate are question-specific expected-work credit, different handling of missing versus wrong submitted answers, and learner/course knowledge state. A useful but **untested** diagnostic hypothesis is weighted credit for correct responses minus a penalty for wrong submissions, with missing answers treated differently. The current samples cannot distinguish that from knowledge-state-dependent credit. Arbitrarily choosing latent question weights could fit the observations but would not constitute reverse engineering.

Public discussion of diagnostic speed-sensitive *placement credit* concerns inferred knowledge, not necessarily XP. It should not be used as an XP formula. The book describes supplemental diagnostics as gathering missing information after knowledge-graph changes, which gives a reason to keep prior knowledge and scope in the candidate model. [The Math Academy Way, pp. 443 and 448–449](https://www.justinmath.com/files/the-math-academy-way.pdf#page=443)

## Reproducing and extending the analysis

- `mathacademy-xp-observations.json`: task IDs/URLs, actual awards/bases, ordered question difficulty/outcomes, missing-answer state, elapsed seconds, selected KP boundaries, and collection metadata.
- `analyze-mathacademy-xp.py`: read-only standard-library analysis using exact `Fraction` arithmetic. It reports predictions, residuals, observed bonus matches, difficulty-count counterexamples, and CSV ceiling counts.
- `mathacademy-xp-model-results.json`: saved output from the final run.

```sh
python3 analyze-mathacademy-xp.py
```

The 12 Assessment and 6 Multistep predictions have zero residuals. All 34 observed IDs and their awards/bases were checked against the CSV. The original CSV was not changed during this XP investigation.

For future extraction, retain `xp_earned` and the displayed baseline as observations. Keep `xp_predicted`, `xp_model`, and `xp_residual` as separate derived fields. Do not replace an observed award with a fitted formula. Expected question times, original planned counts, per-KP stopping/mastery state, and prior penalty count are the highest-value missing inputs for explaining the remaining types.
