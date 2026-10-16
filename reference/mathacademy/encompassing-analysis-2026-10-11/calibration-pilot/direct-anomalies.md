# Audit of direct-review anomalies

This audit uses the frozen 2026-10-11 reports. Accounts are independent; the counts below are audit totals, not pooled calibration data. No engine or database values were changed.

All eight unusual transitions are present in saved raw topic-circle HTML and match the saved parsed color. Each before/after comparison uses the same account, course and topic; the timestamps bracket one captured completed activity. **No pairing or color-parsing bug was found.** This establishes the displayed change, not its private numeric meaning.

| Account | Task | Topic | Display | Correctness | Matching courses | Same activity: rises / falls |
|---|---:|---|---|---|---|---|
| foundations | 13956515 | 775: Ordering Objects | 3→2 | WCWCC | 111 | 17 / 3 |
| foundations | 14055537 | 803: Graphing Curves Defined Parametrically | 3→2 | CWCWC | 136 | 8 / 4 |
| foundations | 14094917 | 730: Expected Values of Discrete Random Variables | 3→2 | WCWCC | 154 | 5 / 9 |
| foundations | 14096422 | 2533: Classifying Equilibrium Solutions of First-Order ODEs | 2→1 | CWCWC | 154 | 11 / 72 |
| foundations | 14097382 | 1730: The Invertible Matrix Theorem in Terms of 2x2 Systems of Equations | 2→1 | CWCWC | 154 | 13 / 10 |
| multivariable | 14117590 | 3022: Conditional Distributions for Continuous Random Variables | 1→6 | CCC | 155 | 8 / 0 |
| differential | 14072669 | 1744: Integration Rules for Vector-Valued Functions | 3→2 | WCWCC | 54 | 0 / 2 |
| differential | 14117289 | 3029: Creating Rows or Columns Containing Zeros Using Gaussian Elimination | 1→6 | CCC | 145 | 1 / 0 |

`C` is a correct answer; `W` is an incorrect answer. All eight tasks passed. The course count is the number of captured courses containing that target, not a claim about courses absent from capture.

## What the decreases show

All six decreased targets also fluctuate in neighboring observations. Differential topic1744 rose1→3 after review14072200 on topic6691 only2.93 minutes before its own review14072669 fell3→2; it rose2→3 again6.41 minutes later. Foundations topic2533 fell2→1 during task14096422 while72 of83 changed target displays fell; its same-start unrelated background averaged−0.571 palette steps. These patterns support allowing a signed background/display component. They do not identify whether that component is ability-dependent display recalculation, asynchronous/stale state, or another hidden update.

The incorrect answers make per-question penalties possible, but do not establish them: most other3/5-correct direct reviews do not fall, and the same targets also fall during other activities. A positive-only completion update followed by a fixed monotone display mapping cannot generate a decrease without such an additional mechanism.

## What the large perfect jumps show

The two1→6 events occurred after the first three questions were correct. Both accounts lack a captured earlier direct practice for the reviewed topic; that means the prior age is unknown, not that this was the learner’s first practice. Differential topic3029 is the only changed target in its activity. Multivariable topic3022 is one of eight rising targets. Neither activity has unrelated background movement. Their signed changes look more specifically associated with the completed practice than the wide falling cohort, but the saved pages do not reveal numeric repetition thresholds, prior latent state, private task quality, or target learning speed.

Do not assign those jumps to long spacing: the required starting time is absent. Do not equate1→6 with five repetitions. Treat them as highest-color observations with uncertain display interpretation and possible large task-quality/ability/initial-state effects.

## Best guess for the cause

The best explanation for the decreases is **recalculation of displayed mastery, probably influenced by ability or performance and sometimes shared across topics**. That explains the rapid reversals and the large falling cohort better than a fixed negative repetition penalty. Incorrect answers can be a trigger within that recalculation; they rank second as a standalone explanation. Asynchronous or stale display state ranks third because the saved evidence contains no demonstrated pairing fault.

For the two perfect jumps, the best explanation is **a large quality/ability-sensitive update on an already-known topic, mapped to the darkest color**. Their prior practice lies outside the observed direct history, so treating them as recent or newly initialized would be the wrong working assumption. The practical model should assign these events a high-gain or uncertain-state tail while learning its usual spacing response from observed ages.

Use those judgments now: fit a signed display residual separately, keep the ordinary positive-credit model for estimating coverage, and publish the resulting best estimates with the later-observation scores. Recovering the private renderer or every hidden parameter is not a prerequisite for the pilot.

## Calibration implication

Fit direct reviews before encompassing. Keep ordinary review gains and an independently calibrated signed residual/exception mechanism separate; preserve these eight observations for predictive checks and sensitivity comparisons. An empirical background effect may be used as a training diagnostic, but the realized after-activity background cannot be used as a predictor for a genuinely future observation. Unknown prior state and the two highest-color jumps need a broad predictive tail or separate uncertain-state component. Fit coverage only after this model assigns plausible predictive probability to both decreases and high jumps.

Accuracy and capture pipeline are confounded: all six decreases are legacy3/5-correct tasks, while the two extreme perfect jumps are current3/3-correct tasks. This supports checking pipeline strata; it does not establish a pipeline bug.

## Evidence

The companion [direct-anomalies.json](direct-anomalies.json) stores all eight exact before/after raw HTML rows, source paths and SHA-256 hashes, question order, matching course IDs, timing, background summaries and adjacent target changes. Source JSONs retain the full raw pages or reference the saved HTML files.

- foundations 13956515: [reference/mathacademy/question-capture/13957832/knowledge-state/lesson-completed.json](/home/jake/Developer/Course_Academy/reference/mathacademy/question-capture/13957832/knowledge-state/lesson-completed.json) → [reference/mathacademy/question-capture/13956515/knowledge-state/review-completed.json](/home/jake/Developer/Course_Academy/reference/mathacademy/question-capture/13956515/knowledge-state/review-completed.json).
- foundations 14055537: [reference/mathacademy/question-capture/14054574/knowledge-state/assessment-completed.json](/home/jake/Developer/Course_Academy/reference/mathacademy/question-capture/14054574/knowledge-state/assessment-completed.json) → [reference/mathacademy/question-capture/14055537/knowledge-state/review-completed.json](/home/jake/Developer/Course_Academy/reference/mathacademy/question-capture/14055537/knowledge-state/review-completed.json).
- foundations 14094917: [reference/mathacademy/question-capture/14094935/knowledge-state/lesson-completed.json](/home/jake/Developer/Course_Academy/reference/mathacademy/question-capture/14094935/knowledge-state/lesson-completed.json) → [reference/mathacademy/question-capture/14094917/knowledge-state/review-completed.json](/home/jake/Developer/Course_Academy/reference/mathacademy/question-capture/14094917/knowledge-state/review-completed.json).
- foundations 14096422: [reference/mathacademy/question-capture/14096234/knowledge-state/lesson-completed.json](/home/jake/Developer/Course_Academy/reference/mathacademy/question-capture/14096234/knowledge-state/lesson-completed.json) → [reference/mathacademy/question-capture/14096422/knowledge-state/review-completed.json](/home/jake/Developer/Course_Academy/reference/mathacademy/question-capture/14096422/knowledge-state/review-completed.json).
- foundations 14097382: [reference/mathacademy/question-capture/14097078/knowledge-state/lesson-completed.json](/home/jake/Developer/Course_Academy/reference/mathacademy/question-capture/14097078/knowledge-state/lesson-completed.json) → [reference/mathacademy/question-capture/14097382/knowledge-state/review-completed.json](/home/jake/Developer/Course_Academy/reference/mathacademy/question-capture/14097382/knowledge-state/review-completed.json).
- multivariable 14117590: [reference/mathacademy/capture/multivariable/14117590/progress-before.json](/home/jake/Developer/Course_Academy/reference/mathacademy/capture/multivariable/14117590/progress-before.json) → [reference/mathacademy/capture/multivariable/14117590/post-activity.json](/home/jake/Developer/Course_Academy/reference/mathacademy/capture/multivariable/14117590/post-activity.json).
- differential 14072669: [reference/mathacademy/question-capture-workers/differential/14072200/knowledge-state/review-completed.json](/home/jake/Developer/Course_Academy/reference/mathacademy/question-capture-workers/differential/14072200/knowledge-state/review-completed.json) → [reference/mathacademy/question-capture-workers/differential/14072669/knowledge-state/review-completed.json](/home/jake/Developer/Course_Academy/reference/mathacademy/question-capture-workers/differential/14072669/knowledge-state/review-completed.json).
- differential 14117289: [reference/mathacademy/capture/differential/14117289/progress-before.json](/home/jake/Developer/Course_Academy/reference/mathacademy/capture/differential/14117289/progress-before.json) → [reference/mathacademy/capture/differential/14117289/post-activity.json](/home/jake/Developer/Course_Academy/reference/mathacademy/capture/differential/14117289/post-activity.json).
