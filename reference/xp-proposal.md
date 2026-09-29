# Proposed XP policy

This is an initial policy for our application, using Math Academy's published design and Jake's recorded activity. It chooses usable rules where the evidence does not determine an exact formula. It is a proposal, not a description of behavior already implemented.

**Recommendation:** treat XP as a reward for a task's expected productive workload, adjusted for performance. Preserve the observed lesson/review bonuses and adopt the assessment and multistep formulas that fit our samples. Use explicit local rules for imperfect practice, diagnostics, and unfinished work. Keep XP separate from accuracy, mastery, and FIRe repetition credit.

## What the evidence supports

I reran [the existing analysis script](analyze-mathacademy-xp.py) against the current [progress.csv](progress.csv). The saved report describes an older 214-row snapshot; the current CSV has **217 tasks**.

| Task type | Current CSV rows | Relevant observation |
|---|---:|---|
| Lesson | 133 | 89 awards equal rounded `1.25 × base`; none exceed it |
| Review | 53 | 38 awards equal `base + 2`; none exceed it |
| Assessment | 13 | Four awards equal rounded `1.2 × base`; none exceed it |
| Multistep | 10 | Five awards equal rounded `1.25 × base`; none exceed it |
| Diagnostic | 6 | No displayed base XP |
| Supplemental diagnostic | 2 | No displayed base XP |

The retained question-level XP sample still contains **34 tasks and 308 questions**. Recalculation reproduces all **12 sampled assessment awards** and all **six sampled multistep awards** with the formulas below. The thirteenth assessment's 18/15 award matches the proposed ceiling, but the reduced XP sample does not contain its outcomes, so it is not a thirteenth question-level formula validation. The CSV contains one negative award, a −1 lesson, and six zero awards. Ceiling matches alone do not prove perfect performance. [Detailed observations](mathacademy-xp-observations.json), [earlier analysis and fit limits](mathacademy-xp-analysis.md).

Math Academy describes XP as expected focused work for a serious average student. Its published bands distinguish perfect, nearly perfect, passable, nearly passable, poor, and deliberately careless work. Passing a lesson with less than maximum XP still means sufficient mastery to move on. That supports a workload baseline and a separate performance adjustment; it does not make earned XP a mastery score. [Gamification](<The Math Academy Way/III-COGNITIVE-LEARNING-STRATEGIES/22-Gamification/22-Gamification.md>), [XP FAQ](<The Math Academy Way/VI-FREQUENTLY-ASKED-QUESTIONS/FAQ-XP-and-Practice-Schedules/FAQ-XP-and-Practice-Schedules.md>).

Three distinctions matter:

- **Base XP is not maximum XP.** Bonuses can exceed the denominator shown on an activity.
- **Actual duration is not an XP meter.** Waiting longer must not earn more. Observed question time divided by base XP varies widely, and historical clocks can include pauses.
- **E/M/H is not a universal 1/2/3-point scale.** That rule already fails captured assessments. Expected workload can vary within a difficulty label.

## Common rules

Let `B` be nonnegative integer base XP, `C` the number of correct questions, `E` incorrect or explicitly skipped questions, and `R(x) = floor(x + 0.5)`. Round once at the end, using exact decimal or rational arithmetic.

A question with several required answer fields counts as one question: correct only when all required fields are accepted. Do not accidentally weight it by the number of fields. Tutorials and examples do not enter question accuracy denominators.

Determine the task's learning outcome independently, then calculate its award. Finalize XP once with the task's completion. Pausing and resuming preserves the attempt. Repeating a completion callback must not award twice.

Initially, **new awards have a floor of zero**. Preserve historical negative awards as recorded. MA's penalties are documented, but their trigger involves inferred carelessness and account history that we have not reconstructed. A speed threshold alone would punish some confident learners and some genuine struggles. Our initial deterrents are fresh questions, no reward for abandonment, persistent required work, and restrictions on paying repeatedly for already satisfied work—not a speculative misconduct detector.

## Lessons

Keep the lesson's mastery rule separate from XP: the proposed practice controller requires two consecutive correct answers within five attempts at each required knowledge point. Passing one knowledge point does not pass the lesson.

For a **passed lesson**, let `K` be its number of assessed knowledge points:

```text
E = 0:        XP = R(1.25 B)
E >= 1:       XP = R(B × max(0.60, 1 − 0.40 × (E − 1) / K))
```

This deliberately simple local rule grants base XP for one mistake, then reduces the award according to additional mistakes relative to lesson size. A passed lesson retains at least 60% of its base because the learner ultimately demonstrated every required skill. Extra recovery questions do not increase `B` or erase previous errors by inflating an accuracy denominator.

For a four-KP lesson worth 16 base XP:

| Result | Award |
|---|---:|
| Passed, no errors | 20 |
| Passed, one error | 16 |
| Passed, two errors | 14 |
| Passed, three errors | 13 |
| Failed the lesson | 0 |

**A failed or abandoned lesson earns zero initially.** Passed KPs and individual answers remain recorded and useful to the engine; zero XP does not mean zero learning. This avoids introducing a second accounting system for repeatedly collecting partial awards on the same early KPs. A later successful attempt uses fresh questions and earns its normal award.

The perfect multiplier and one-error base award have direct support. The slope, 60% floor, and zero failed-lesson award are our choices, not fitted MA coefficients. MA's public description allows a small award for nearly passable performance; its unpublished task-level decision could be more generous. Captured lesson question sequences and XP do not reliably identify their internal pass/fail states. In particular, the historical `CICIC` group must not be labeled a successful two-consecutive-correct KP merely because the page says “Completed.”

This rule will not reproduce every old partial lesson award. That is preferable to disguising an arbitrary overfit as a recovered formula.

## Reviews

Use the [scheduling proposal](scheduling-proposal.md)'s practice controller: at least three questions, stop successfully when the last two are correct, and stop after five questions at most. This differs from the current code's three-consecutive-correct rule, which cannot explain captured three-question `ICC` reviews.

| Terminal performance | XP |
|---|---:|
| First three questions all correct | `B + 2` |
| Passed with one error | `B` |
| Passed with two or more errors | `R(0.75 B)` |
| Did not pass by question five, at least three correct, final answer correct | `R(0.5 B)` |
| Other failed review | `0` |

`C` means correct and `I` means incorrect in these examples:

| Captured sequence | Base | Proposed / observed XP |
|---|---:|---:|
| `ICC` | 4 | 4 / 4 |
| `CCICC` | 4 | 4 / 4 |
| `ICC` | 6 | 6 / 6 |
| `CCIIC` | 4 | 2 / 2 |
| `CCICI` | 6 | 0 / 0 |
| `CCC` | 7 | 9 / 9 |

This reproduces all six inspected reviews. The half-award distinction treats a final correct answer as partial recovery, without treating the review as passed. That interpretation and the 75% band are proposed application rules; the results pages do not expose MA's actual stopping or pass/fail decision. The `+2` bonus is observed only for bases 4–7. Extending it to other bases is an intentional simple default.

An unsuccessful review can therefore earn a little XP while still triggering the engine's failure/remediation path. There is no contradiction: XP acknowledges useful work; the review outcome decides whether the required retention evidence was supplied. Partial XP does not discharge required work.

## Assessments

Adopt the fitted rule:

```text
p = C / N
XP = max(0, R(1.2 B × (p − 0.35) / 0.65))
```

For a normally completed assessment, `N` is the number of questions in its fixed definition. Give equal weight to questions. The sample does not support universal E/M/H weighting.

At base 15:

| Accuracy | XP |
|---|---:|
| 100% | 18 |
| 90% | 15 |
| 75% | 11 |
| 60% | 7 |
| 35% or below | 0 |

The 35% crossing and 20% perfect multiplier are a compact exact fit to the 12 sampled awards, not uniquely identified constants. They are strong enough to adopt as our initial policy.

If time expires, keep `N` equal to the full prepared assessment size. Unanswered questions receive no scoring credit. **Do not fabricate incorrect or skipped task items for unpresented questions.** This is a task-level score denominator, distinct from observed answer accuracy. Scoring only presented questions would let answering one easy question and stopping produce a perfect award. Initially there is no separate early-submit action: complete all questions, allowing explicit skips, or reach the real time limit. Abandonment does not finalize an assessment award or clear its requirement.

An assessment completion can earn zero and still fulfill the obligation to provide assessment evidence. Incorrect answers drive remediation separately. A later assessment uses the same formula; its title or resemblance to a previous assessment does not create a special retake formula.

## Multistep tasks

Adopt the fitted formula with a zero floor:

```text
p = C / N
XP = max(0, R(B × (2.25p − 1)))
```

`N` counts the assessable question steps in the prepared task, not instructional steps. The unclamped formula matches all six inspected awards. The zero floor is our extension: no inspected multistep falls below 5/9 correct, so negative extrapolations are unsupported.

At base 10, perfect work earns 13; 80% earns 8; 60% earns 4; 40% earns zero. If the task supports a legitimate early final submission, unanswered question steps remain in `N`. Abandonment earns zero.

## Diagnostics

Do not apply the assessment accuracy cutoff to a diagnostic. A diagnostic intentionally explores the boundary between known and unknown material; honest “I don't know” responses are useful. The captured diagnostic with three correct answers out of 16 still earns positive XP, directly contradicting the assessment formula as a universal scoring rule.

Use **expected-work credit for successful probes**:

```text
XP = R(sum(reference expected seconds of successful counted probes) / 60)
```

Incorrect and explicitly skipped probes earn no XP and incur no penalty. Unselected branches have no effect. Credit only the final result of a probe/retry pair, and at most one success for that probe. If the learner takes a silly-mistake retry, the retry replaces the original for the knowledge frontier, as requested; the original response remains in history. It does not create a second XP opportunity.

For example, successful counted probes with expected times of 60, 90, and 120 seconds earn five XP after rounding. Answering those probes more slowly does not increase the award. Explicit completion or time expiry finalizes the award; pausing does not. Abandonment earns zero.

This is our rule, not a fit to historical diagnostic awards. The available examples show that a shared fixed reward per correct E/M/H answer cannot explain MA's diagnostic and supplemental results. Question-specific expected work offers a useful initial scale without penalizing honest frontier discovery. The same rule works for a diagnostic of any scope; a separate supplemental-diagnostic XP model is unnecessary.

## Assigning base XP to generated activities

Preserve imported base XP where it exists. For newly generated work, calculate `B = max(1, R(reference expected seconds / 60))` before starting, then freeze it on the learner task.

Use the same **reference workload estimates** as the scheduler, before any adjustment for the current learner's speed:

- **Lesson:** tutorial/example reading time plus three expected questions per required KP. Three is our initial allowance for a serious but imperfect learner; delivery can still stop after two or continue to five.
- **Review:** expected time for the initial three questions. Reserve five fresh questions for adaptive delivery, but do not price every review as if all five will be needed.
- **Assessment:** expected time of every selected question. A fifteen-minute limit does not force fifteen base XP if the selected work has a different expected duration.
- **Multistep:** expected instructional time plus expected time for its question steps.

Content-author estimates are the starting point. Use robust observed times to improve them when clean observations exist. A personalized scheduler duration can be shorter or longer than the reference duration without changing the learner's reward for the same work.

Until estimates exist, use the scheduling proposal's explicit provisional defaults: 12 minutes for a lesson, six for a review, and 90 seconds per question for a newly assembled assessment, multistep, or diagnostic. Do not infer timings from E/M/H alone. These are working estimates to replace as content is reviewed, not claims about MA or universal mathematical workload.

Expected-time estimates need a shared application interface. That does not justify copying generator scripts, grading machinery, or learner timings into the XP schema. At present, `learner-task/xp-base` and `learner-task/xp-earned` already store the necessary baseline and award.

## Avoiding farming and keeping the engine coherent

Recommended, required, and self-selected **eligible learning work use the same award rules**. A new self-selected lesson receives its normal base and performance adjustment.

Do not pay a second first-learning award for rerunning an already learned lesson. Route a needed revisit through review/remediation, or allow optional extra practice with no task XP. Likewise, ordinary review XP is for due or assigned remedial work; generating endless fresh questions for an already satisfied review must not create endless rewards. This is a reward eligibility distinction, not a ban on choosing extra practice. Make it visible before starting.

Prevent repeat questions using the learner's presentation history and atomic presentation reservation. Count questions seen in unfinished, skipped, and abandoned work as seen. Generating a new question UUID for identical content must not evade the bank's duplicate check. An already displayed question may remain visible when resuming its original task; it is not a new earning opportunity.

Finalize the task award exactly once. Resuming, replaying callbacks, or recalculating a screen cannot add XP. The historical task award is authoritative; future tuning changes future awards, not old records.

For the assessment cadence, count `max(0, xp-earned)` from finalized lessons, reviews, and multisteps since the last completed assessment. Exclude assessment and diagnostic XP. At 150 accumulated XP, require an assessment. Completion, including timer expiry, resets that cadence to zero regardless of its score; abandonment does not. Maintain at most one outstanding cadence obligation. This matches the [scheduling proposal](scheduling-proposal.md) and is a local policy rather than an observed exact MA counter.

XP does not become FIRe repetitions, memory, evidence mass, or mastery. Individual answer results update performance; the learning controller determines mastery and retention evidence; the XP function awards the task. A learner can earn review XP without learning a new topic, or finish a low-scoring assessment that supplies valuable evidence.

## Changes implied by accepting this proposal

The current [activity helpers](../engine/activities.py) only calculate perfect lesson/review candidates, while assessment/multistep fits are opt-in. [The runtime](../engine/runtime.py) still leaves other awards to an explicit caller and does not implement this proposal's complete scoring policy.

Implementation would replace those gaps with these task calculators, freeze base XP at task launch, use the prepared-question denominator for timed assessment scoring, and share reference duration estimates and reward eligibility with scheduling. Keep the coefficients in ordinary application configuration initially. They are not FIRe retention parameters, and no new XP ledger or additional EDN schema is required for the rules above.
