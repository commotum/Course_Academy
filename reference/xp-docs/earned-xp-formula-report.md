# Earned XP from question accuracy

Research date: October 4, 2026. This report extends the [base-XP investigation](base-xp-formula-report.md) using completed-task awards and question outcomes.

**Result:** a small set of formulas using task type, base XP, and whole-task accuracy reproduces **131 of 134 observed awards exactly**. It reproduces **131 of 132 nonnegative awards**, including every nonnegative lesson, quiz, and multistep award in the sample. The formulas are cheap approximations fitted to all available observations, not recovered Math Academy code.

Accuracy alone cannot explain every award: two reviews have identical base XP, correct count, and total question count but different XP. Negative penalties also require a separate policy that this sample does not identify.

**Follow-up:** allowing one answer-order condition raises agreement to **132/134 overall and 132/132 nonnegative awards**. For reviews below two-thirds accuracy, a final incorrect answer predicts zero XP. The evidence and its limits are documented in [Answer order and difficulty](#answer-order-and-difficulty).

## What Math Academy publicly says

Math Academy describes full credit for getting most lesson answers right, partial credit for getting some right, and negative XP when it detects rushing or guessing. Its FAQ does not publish an equation or say that the aggregate correct fraction is the only scoring input. [Math Academy FAQ](https://mathacademy.com/faq)

The book describes distinct reward bands for perfect, nearly perfect, passable, nearly passable, poor, and careless performance. Its diagram includes a jump at passing, without numerical thresholds. This allows a task-outcome adjustment in addition to accuracy. [The Math Academy Way, chapter 22](https://www.justinmath.com/files/the-math-academy-way.pdf#page=312)

A staff discussion also describes penalties being capped during an introductory period and increasing after repeated penalties. The speaker qualifies the particular numeric schedule as a recollection. This supports account history as an additional input, but does not establish the current penalty implementation. [Math Academy Podcast #2, 48:55](https://www.justinmath.com/math-academy-podcast-2/)

Therefore, “earned XP is strongly adjusted for accuracy” is supported. “Earned XP is determined solely by accuracy” is too strong.

## Data and method

The frozen snapshot was collected at `2026-10-04T21:41:01.613115+00:00`. It combines **105 completed capture activities** with **29 historical activities** from the earlier question-level XP investigation: **134 activities and 1,439 question occurrences**. The two sources have no overlapping task IDs.

| Task type | Activities | Accuracy coverage |
|---|---:|---|
| Lesson | 63 | 58 captures at 60%; five historical tasks at 25%, 75%, 76.9%, 88.9%, and 100% |
| Review | 46 | 60%, 66.7%, 80%, and 100% |
| Quiz / assessment | 16 | 0% through 100%; includes one entirely unanswered expired quiz |
| Multistep | 9 | 55.6% through 100% |

All 105 included capture activities had their question counts, IDs, and outcomes checked against retained completed-activity metadata. Their displayed completion text supplies both the base and earned XP. Where state also stores an earned-XP field, it must agree with that text.

Excluded records are explicit in [observations.json](../mathacademy-earned-xp/observations.json): review `13929099` lacks a recoverable base/earned pair in its saved completion text; multistep `13942110` was unfinished; five historical diagnostic activities have no displayed base. Their exclusion does not imply that their awards fit these formulas.

As requested, all qualifying observations were used together. There was **no holdout, cross-validation, or separate test set**. Reported percentages measure agreement with these recorded awards, not accuracy on unseen learners or future activities. No live questions were answered for this investigation.

## Definitions

- `B`: base XP, the displayed task denominator, whether observed directly or estimated separately.
- `C`: number of correct question occurrences.
- `N`: number of scored question occurrences.
- `p = C/N`: whole-task accuracy, between zero and one.
- `R(x) = floor(x + 0.5)`: nearest-integer rounding with half ties upward. Round once, at the end.
- `clamp(x, 0, 1) = max(0, min(1, x))`.

Each question counts once, even if it has several answer fields. Tutorials and examples do not enter `N`. For a fixed quiz, use the full assigned question count, including unanswered questions when time expires. This is a scoring denominator, not merely the number of submitted responses. Capture activity `13939908`, for instance, has seven correct answers out of eight assigned questions, with the eighth unanswered.

The only learner-performance input is `p`. Task type and `B` remain necessary: the same accuracy can receive different treatment in a lesson and quiz, and different workloads have different bases. Difficulty, response time, priorities, and learner mastery facts do not enter these earned-XP approximations.

## Selected formulas

### Lessons

```text
if p == 1:
    XP = R(1.25 B)
else:
    XP = R(B × clamp(1.4p − 0.24, 0, 1))
```

This matches **62/62 nonnegative lesson awards**. The only mismatch among all 63 lessons is the historical negative award discussed below.

The strongest observation is at `p = 0.6`: every one of the 58 captured lessons earns exactly `R(0.6 B)`, across bases from 7 to 25. These captures deliberately used sequences with three correct answers in five attempts per knowledge point. They are a broad check of the base scaling and rounding at one accuracy, not 58 independent checks of the curve at different accuracies.

To extend that anchor, we considered an imperfect-lesson line:

```text
multiplier = min(1, 0.6 + a × (p − 0.6))
```

The older nonnegative imperfect lessons constrain the slope to:

```text
91/66 ≤ a < 14/9
1.378787… ≤ a < 1.555555…
```

Choosing the simple value `a = 1.4` fits all of them and yields `1.4p − 0.24`. The cap gives full base at about 88.57% accuracy; perfect performance uses the separate 25% bonus.

| Historical task | Base | Correct / total | Observed XP | Formula |
|---|---:|---:|---:|---:|
| 13471622 | 15 | 9/12 | 12 | 12 |
| 13497944 | 9 | 10/13 | 8 | 8 |
| 13510941 | 19 | 8/9 | 19 | 19 |
| 13512234 | 16 | 8/8 | 20 | 20 |

The slope, intercept, and exact plateau threshold are **our fitted choices**. Nearby slopes also reproduce the rounded awards. Accuracy below 60% has no nonnegative lesson observation in this sample; the lower part of the clamped line is unsupported extrapolation. Neither this line nor a green completion checkmark identifies the internal pass/fail decision.

### Reviews

```text
if p == 1:
    XP = B + 2
elif p >= 2/3:
    XP = B
else:
    XP = R(Bp)
```

This matches **45/46 review awards**. All 40 included capture reviews had 3/5 accuracy and match `R(0.6 B)`; the historical sample adds observations at 2/3, 4/5, and perfect accuracy.

The exact boundary is not identified: choosing `2/3` is a simple way to separate the observed 60% partial-credit cases from the 66.7% full-base cases. The perfect `+2` rule is directly supported by the historical perfect base-7 review; broader historical CSV ceiling matches provide supporting evidence without known outcomes for every row. It remains indistinguishable from some minimum-bonus percentage policies over the small observed base range.

**An exact accuracy-only formula is impossible for these retained review observations:**

| Task | Base | Correct / total | Ordered outcomes | Earned XP |
|---|---:|---:|---|---:|
| 13409092 | 6 | 3/5 | `CCICI` | 0 |
| 13938605 | 6 | 3/5 | `CICIC` | 4 |

Here `C` means correct and `I` means incorrect. Both have identical inputs even if correct count and total are provided separately. A deterministic formula using just type, base, and aggregate accuracy must produce the same prediction for both. The selected rule predicts 4, matching the newer capture and missing the historical task by 4 XP.

The different final outcomes make termination or recovery state a plausible explanation. Difficulty, internal objectives, historical policy changes, or other state could also contribute. The pair proves that an additional input is needed; it does not prove which one.

### Quizzes / assessments

```text
XP = max(0, R(1.2 B × (p − 0.35) / 0.65))
```

This matches **15/15 nonnegative quiz awards**, extending the earlier 12-task fit with three newer normally scored quizzes. Perfect accuracy gives a 20% bonus. The inferred zero crossing is 35%; the full-base crossing before rounding is about 89.17%.

The 35% crossing is a convenient rounded-output fit, not a published cutoff. Nearby values also fit the observations. The remaining quiz expired with no answers and earned −1 XP; the zero-clamped formula predicts zero.

### Multistep tasks

```text
XP = R(B × (2.25p − 1))
```

This matches **9/9 multistep awards**, extending the earlier six-task fit with three newer perfect captures. Perfect accuracy gives a 25% bonus.

No observed multistep falls below 55.6% accuracy. The line becomes negative below about 44.4%; its behavior there and any penalty cap are unverified. If our application elects to floor this at zero, that is a local policy choice and gives the same predictions on the observed multisteps.

## Fit quality and exceptions

| Type | Exact matches, all awards | Mean absolute error | Exact matches, nonnegative awards |
|---|---:|---:|---:|
| Lesson | 62/63 | 0.0476 XP | 62/62 |
| Review | 45/46 | 0.0870 XP | 45/46 |
| Assessment | 15/16 | 0.0625 XP | 15/15 |
| Multistep | 9/9 | 0 XP | 9/9 |
| **Total** | **131/134 (97.8%)** | **0.0597 XP** | **131/132 (99.2%)** |

The maximum error is 4 XP. All three exceptions remain visible in the results:

| Task | Type | Base | Correct / total | Actual | Predicted |
|---|---|---:|---:|---:|---:|
| 12601433 | Lesson | 14 | 1/4 | −1 | 2 |
| 13409092 | Review | 6 | 3/5 | 0 | 4 |
| 13933898 | Assessment, expired | 15 | 0/9 | −1 | 0 |

The high agreement is dominated by deliberately repeated 60% capture policies: 98 activities sit at that accuracy. It should not be interpreted as identifying the shape of the reward curve throughout the accuracy range. Combining historical and newer records also assumes the main award rules are comparable across dates; a policy change is another possible explanation for the review discrepancy.

A plain `R(Bp)` rule matches only 102/134 awards. The selected formulas improve this to 131/134 without using question difficulty, elapsed time, topic identity, or fitted parameters for individual tasks. No observed award was replaced or changed.

## Example at base XP 15

These are formula outputs; most combinations are illustrative rather than directly observed.

| Accuracy | Lesson | Review | Quiz | Multistep |
|---|---:|---:|---:|---:|
| 60% | 9 | 9 | 7 | 5 |
| 75% | 12 | 15 | 11 | 10 |
| 80% | 13 | 15 | 12 | 12 |
| 90% | 15 | 15 | 15 | 15 |
| 100% | 19 | 17 | 18 | 19 |

## Runtime use and reproduction

[estimator.py](../mathacademy-earned-xp/estimator.py) implements the four candidates with exact integer arithmetic, including ties-upward rounding. It needs no external packages. Measured locally over repeated calls, the public estimator takes approximately **0.7–0.9 microseconds per call**, including input validation. Its inputs are `kind`, `base`, `correct`, and `total`.

```python
estimate_earned_xp("lesson", base=15, correct=9, total=15)  # 9
estimate_earned_xp("assessment", base=15, correct=7, total=10)  # 10
```

The prototype is not integrated into the learner engine or capture script. It rejects diagnostic types because no corresponding base-relative formula has been identified. Keep observed XP separate from predicted XP. Any negative-penalty policy, task-state adjustment, or treatment of abandonment should remain explicit rather than being disguised as an accuracy coefficient.

The fit uses observed bases to isolate the performance adjustment. Substituting the [estimated base](base-xp-formula-report.md) adds that model's error; the 97.8% agreement does not describe the combined base-and-earned estimator.

Artifacts:

- [Frozen observations](../mathacademy-earned-xp/observations.json): awards, bases, ordered outcomes, source hashes, and exclusions.
- [Results](../mathacademy-earned-xp/results.json): per-task predictions, comparisons, slope interval, identical-input conflicts, and every mismatch.
- [Analysis script](../mathacademy-earned-xp/analyze.py): extraction and whole-data agreement calculations using only Python's standard library.
- [Earlier investigation](../mathacademy-xp-analysis.md): historical collection context and the original quiz/multistep hypotheses.

Reproduce against the frozen observations:

```bash
python reference/mathacademy-earned-xp/analyze.py
```

Use `--refresh` to replace the frozen observations with the current completed local captures and recalculate agreement. This refreshes evidence for the stated formulas; it does not automatically refit their coefficients or thresholds. Capture source files, progress CSV, and learner database facts remain untouched.

## Answer order and difficulty

The follow-up compared simple sequence and difficulty hypotheses on the same entire frozen sample. No new activities were performed and no observations were held out.

The strongest explanation of the review exception is its terminal outcome. Keep the existing accuracy rule, with this additional condition:

```text
if task_type == review and p < 2/3 and final_answer_is_incorrect:
    XP = 0
else:
    use the accuracy-only formula
```

This distinguishes `CCICI` (zero XP) from `CICIC` (partial XP). It also preserves partial XP for `CCIIC`, despite that sequence containing two consecutive mistakes. The condition improves the review fit from 45/46 to 46/46 and the overall fit from 131/134 to 132/134. All 132 nonnegative awards now match.

**Confidence limit:** the sample has only one review that both finishes incorrectly and has below-two-thirds accuracy. The rule is consistent with a failure-versus-partial-recovery distinction, but may be a proxy for hidden task state. It is an exploratory extension, not an identified universal stopping or scoring rule. Applying a final-wrong zero rule to every activity would be incorrect: quiz `13939908` ends unanswered yet earns its full 15 base XP at 7/8 accuracy.

### Candidate comparisons

Each modification below uses the existing review formula and is evaluated against all 46 reviews.

| Candidate | Exact review awards |
|---|---:|
| Original accuracy-only rule | 45/46 |
| Below two-thirds accuracy and final answer incorrect → zero | **46/46** |
| Below two-thirds accuracy and any two consecutive mistakes → zero | 44/46 |
| Below two-thirds accuracy and at least two easy-question mistakes → zero | 37/46 |
| Substitute difficulty-weighted accuracy, E/M/H = 1/2/3 | 26/46 |
| Substitute difficulty-weighted accuracy, E/M/H = 1/2/4 | 23/46 |

The weighted comparisons change accuracy inside the existing review rule without refitting its thresholds. They reject those straightforward substitutions, not every possible difficulty-dependent model.

At 60% accuracy, the reviews contain between zero and five easy questions. Every included capture review still earns `R(0.6B)`. The zero-XP historical review contains two easy questions and answers both correctly; its two mistakes are moderate questions. Conversely, all-easy review `13930486` misses two easy questions and still earns 2/4 XP. Easy-question count and easy mistakes therefore provide no strong explanation of the exception in this sample.

Two consecutive mistakes are also a poor discriminator: the zero-XP review has **no** consecutive mistakes (`CCICI`), while review `12698374` contains two (`CCIIC`) and earns 2/4 XP.

### Remaining negative awards

| Task | Type | Correct / total | Outcomes | Longest wrong run | Easy questions / easy mistakes | Award |
|---|---|---:|---|---:|---:|---:|
| 12601433 | Lesson | 1/4 | `IICI` | 2 | 1 / 0 | −1 |
| 13933898 | Expired quiz | 0/9 | `IIIIIIIII` | 9 | 5 / 5 | −1 |

For the expired quiz, all nine questions are recorded as unanswered; the sequence does not represent nine submitted wrong responses. Complete nonparticipation is a plausible penalty trigger. The lesson has very low accuracy and ends incorrectly, making an unsuccessful early termination a plausible trigger. Its only easy question was answered correctly, so easy mistakes cannot explain its penalty.

Consecutive errors alone cannot determine a negative award: historical quiz `4833336` ends with **five** consecutive incorrect outcomes and still earns 2/12 XP. Quiz `12225370` has a run of three, ends incorrectly, and earns zero rather than a penalty.

The strongest working hypothesis is therefore **accuracy plus terminal task state, followed by a separate penalty policy**. For the negative cases, the recorded −1 might reflect an account-level cap rather than a raw task score. We cannot infer the penalty threshold or uncapped amount from these two examples, and a universal −1 rule would simply memorize them.

### Artifacts

- [Sequence and difficulty results](../mathacademy-earned-xp/sequence-results.json): candidate match counts, per-task features, remaining exceptions, and easy-count distribution.
- [Comparison script](../mathacademy-earned-xp/sequence_analysis.py): reruns all candidate comparisons using the frozen observations.
- [Estimator](../mathacademy-earned-xp/estimator.py): retains the accuracy-only function and adds `estimate_earned_xp_with_sequence(kind, base, outcomes)`, taking ordered boolean outcomes. The added function applies only the exploratory review condition; it does not invent negative penalties.

```bash
python reference/mathacademy-earned-xp/sequence_analysis.py
```

All included capture reviews' stored question order was checked against their completed-activity metadata. Neither scoring variant has been integrated into the learner engine or capture script.

## Investigating negative XP

A closer examination identified a third confirmed negative award outside the base-relative fit. Review `13929099` has no recovered base in its completion text, so it remains excluded from the numerical dataset. Its **−1 earned XP** is independently retained in the [following queue snapshot](../mathacademy/question-capture/13929417/queue-after.json), and its outcomes and difficulties are present in [completed-activity metadata](../mathacademy/question-capture/13929099/activity-metadata.json).

| Task | Activity | Accuracy / outcome | Additional evidence |
|---|---|---|---|
| 12601433 | Left and Right Riemann Sums in Sigma Notation | 1/4, `IICI`, −1/14 XP | Wrong moderate, wrong hard, correct easy, wrong moderate. Displayed question times: 305, 166, 553, and 224 seconds. |
| 13929099 | The Argument of a Complex Number, review | 2/5, `CICII`, −1 XP | All five questions easy. Displayed question times: 11, 19, 12, 12, and 23 seconds. Base remains unidentified. |
| 13933898 | Quiz 7 | 0/9 answered, expired, −1/15 XP | A capture layout error and subsequent navigation timeouts preceded recovery of the expired quiz. |

The lesson's displayed times sum to **20 minutes 48 seconds**, exceeding its 14 base XP. Each wrong answer shows at least 166 seconds. This does not look like an obvious fast-guessing pattern, although displayed times can include pauses and do not establish effort or intent. Its very low accuracy and terminal error are more evident than rushing. The only easy question was correct.

The review provides an informative nearby comparison: another all-easy review, `13930486`, scored 3/5 and earned 2/4 XP. Holding the easy-question count at five therefore still allows partial versus negative awards. Accuracy and terminal state are stronger candidates than easy-question count alone. The negative review ends with two mistakes, but two consecutive mistakes also occur in positively awarded reviews, so that feature needs task-state or accuracy context.

For Quiz 7, the [first error record](../mathacademy/question-capture/13933898/diagnostics/1791114247741724783/error.json) reports `Unknown assessment navigation layout`. Later diagnostics report navigation timeouts. Its [saved state](../mathacademy/question-capture/13933898/state.json) records an expired submission with all nine questions unanswered. This is evidence about a task started without successful participation, associated with a technical capture failure. It cannot isolate a low-accuracy penalty from an expiry or abandonment penalty.

Math Academy's FAQ explicitly distinguishes an ordinary struggling learner whose lesson is cut short for zero XP from detected rushing or guessing that receives negative XP. That description supplies possible mechanisms; our records do not expose the detector or show that it classified these particular activities correctly. [Official XP explanation](https://mathacademy.com/faq)

### Separate eligibility from amount

A useful working model asks two questions:

```text
Does this task qualify for a penalty?
If so, what raw penalty is indicated, and what history-dependent cap applies?

possible award = −min(raw_penalty, account_penalty_cap)
```

This is an investigative decomposition, not a recovered implementation. A cap of zero could turn an eligible penalty into a zero award; a cap of one could make several different raw penalties all appear as −1. The staff discussion of introductory penalty caps makes this plausible. [Podcast #2, 48:55](https://www.justinmath.com/math-academy-podcast-2/)

All three confirmed negative awards are −1, which is consistent with a capped phase but does not prove one. The retained historical CSV contains four zero-XP practice/quiz activities before the August 21 negative lesson, plus a zero diagnostic. These cannot be counted as five prior penalties: some may be ordinary zero awards, and the diagnostic is a different activity type. Complete chronological history and a reason indicator would be needed to reconstruct a penalty counter.

### What evidence would distinguish the causes

1. **Recover the zero-award activities' outcomes and terminal messages.** The highest-value historical tasks are `4866773`, `11637108`, and `12225753`, whose question sequences are absent from the retained XP sample. Compare them with the negative activities within the same task type. For example, very low accuracy ending incorrectly with slow responses but zero XP would weaken a task-local accuracy-only explanation and make a history cap more plausible.
2. **Separate wrong submissions from no participation.** Retain assigned, displayed, submitted, and unanswered counts, skip/expiry/abandonment status, start/finish times, and exact final-screen or history wording. “No answer” alone does not distinguish deliberate skipping from timeout or technical failure.
3. **Track sequence and per-KP termination.** Retain mistake runs, the final answer, successes after errors, and whether a required KP or the whole task was stopped early. This can distinguish unsuccessful completion from partial recovery at the same accuracy.
4. **Use timing only as a candidate penalty feature.** Compare actual active response time with expected question time when available; total elapsed time and base XP are imperfect substitutes. Timing need not enter ordinary earned XP to affect a separate penalty detector.
5. **Reconstruct account-level history.** Order prior negative and zero awards and preserve any penalty-specific messages. Equal task performance changing from zero to −1 or −2 over time would support escalation, but zero awards must first be classified as possible capped penalties versus ordinary zero credit.

These comparisons should use saved evidence and naturally occurring outcomes. Repeated captures of intentionally failed activities would alter both the remote knowledge state and the suspected penalty history, making the comparisons harder to interpret. With the current three examples, neither a reliable trigger threshold nor an uncapped penalty amount is identified.
