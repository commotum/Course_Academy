# Potential functions: two different kinds of displayed gain

The best explanation of the late event is **reassessment or revalidation of component knowledge during relearning in a new course context**. The late `1→6` gain persisted; the earlier `1→3` gain was part of rapidly changing display state. Neither event supports treating its jump size as newly earned ordinary repetition credit.

This audit uses only the multivariable account's 593 tasks in the frozen [source report](../multivariable.json). The [machine-readable evidence](case-study.json) records every relevant course observation, source hashes, selected HTML checks, and question-level correctness. No other account contributes evidence.

## The early gain reverses in 32.6 minutes

These are original course-54 reads, rather than changes copied between baselines. Times are UTC on October 9, 2026.

| Read after task | Time | Source activity | Potential functions 1951 | Conservative fields 3149 |
|---|---|---|---:|---:|
| 14067931 | 02:56:13 | Review, double integrals in polar coordinates | 1 | 2 |
| 14068004 | 02:58:53 | Review, fundamental theorem for line integrals 2110 | 3 | 2 |
| 14068383 | 03:31:29 | Lesson, principal normal vectors 1795 | 1 | 2 |
| 14068563 | 03:42:09 | Review, interpreting line integrals 3694 | 3 | 2 |
| 14068638 | 03:48:25 | Lesson, parameterization by arc length 1838 | 1 | 2 |
| 14068604 | 03:51:40 | Direct review of potential functions 1951 | 3 | 2 |

The exact first-rise-to-first-reversal interval is **32.5957 minutes**. Potential functions remains at 3 in five intervening post-activity reads, then falls to 1. The sequence does not merely occur in extracted JSON: the saved `units_html` contains the corresponding topic-circle colors at each listed reversal. This rules out a simple color-parser mistake. It does not distinguish a changing server-side state from stale or asynchronous responses.

The oscillation continues as numerous `2↔3` changes across later activities. A positive-completion-credit model with a fixed monotone mapping from repetitions to bands cannot explain those reversals on its own. The first visible `1→3` gain therefore cannot be used as evidence that this relationship permanently added two repetition units.

## The late gain is persistent and selective

The chronological context is more specific than “previously strong knowledge.”

| Stage | Time, UTC | Course page for components | Potential functions 1951 | Conservative fields 3149 | Source 2110 |
|---|---|---:|---:|---:|---:|
| Immediately preceding saved profile, after task 14097330 | Oct 10, 15:10 | 54 | 3 | 3 | 1 |
| After Differential Equations diagnostic 14097559 | Oct 10, 21:18 | 54 | 5 | 6 | 1 |
| After Mathematical Methods for the Physical Sciences II diagnostic 14111253 | Oct 11, 12:08 | 154 | 1 | 1 | 0, on course 155 |
| Last baseline before lesson 14119320 | Oct 11, 14:54 | 154 | 1 | 1 | 0, on course 155 |
| After lesson 14119320 | Oct 11, 15:03 | 154 | 6 | 6 | 1, on course 155 |
| Last observation in frozen window, after task 14124541 | Oct 11, 21:10 | 154 | 6 | 6 | 1, on course 155 |

The older `5/6` values are **display bands in saved HTML after an earlier diagnostic**, not an independent numeric learner-repetition profile. Both components were 3 in the preceding saved snapshot. Thus the earlier high state was itself assigned during a diagnostic interval; it is not evidence that five or six ordinary repetitions had accumulated.

The course change has activity evidence, not merely a different panel list. Task 14097559's `state.json` identifies the Differential Equations placement exam, course 61. Task 14111253's `activity.json` identifies the Mathematical Methods for the Physical Sciences II placement exam, course 155. Task 14119320's activity metadata also gives course 155, and its captured dashboard reports current course 155. The early review's saved sidebar selects Multivariable Calculus, course 54; its legacy activity state does not contain an explicit course ID. The component reads move from course page 54 to page 154 across this history, so the `5/6→1/1` comparison is not a same-course observed reset.

The late lesson's [baseline](../../capture/multivariable/14119320/progress-before.json) and [completion observation](../../capture/multivariable/14119320/post-activity.json) show only four changed topics:

- Fundamental theorem for line integrals 2110: `0→1`.
- Calculating potential functions 1951: `1→6`.
- Conservative vector fields 3149: `1→6`.
- Gradient vector 1934: `4→5`.

Both components were 1 in **28 original course-154 observations before the lesson**, beginning with the new diagnostic. Both were 6 in **40 observations including lesson completion**, or **39 later observations**, spanning **6.1031 hours**. These counts are reproducible within the frozen capture window. A next activity's `progress-before.json` repeats the previous original course-read timestamp and is not another observation; neither are observation-history or repair copies. Identical bands observed at different original timestamps do count as repeated evidence of persistence.

This selective, sustained change favors a component reassessment associated with the lesson over a brief display glitch. Revalidation is a better description than exact restoration: potential functions previously displayed 5, whereas the later value is 6. Revalidation plus ordinary credit, or a reassigned category, can account for that distinction.

## Correctness does not explain the difference by itself

The source's mathematical overlap with potential-function reconstruction depends on the question. When the potential is supplied, evaluating endpoint values does not reconstruct it. The “potential function is not given” KP does reconstruct it. The saved questions and solutions support that distinction.

| Activity | Potential supplied: correct / attempted | Potential not given: correct / attempted | Potential-functions band |
|---|---:|---:|---|
| Earlier lesson 14059357 | 6/10 across two KPs | 3/5 | `1→1` |
| Review 14065132 | 3/3 | 0/2 | `1→1` |
| Review 14068004 | 3/3 | 0/2 | `1→3`, then reverses |
| Relearning lesson 14119320 | 6/10 across two KPs | 3/5 | `1→6`, then persists |

The two reviews have identical KP-level counts. The two lessons also have identical KP-level counts. Consequently the differing bands cannot be explained simply by better accuracy on the reconstruction KP. The late lesson does successfully practice reconstruction three times, which makes a revalidation trigger plausible; it does not imply a larger mathematical encompassing fraction.

There is additional direct evidence of prior successful reconstruction in the new context. Diagnostic 14111253 includes question `q-104725`, sequence position 57, on source topic 2110's **potential-not-given** KP. Its saved history and live feedback both say **Correct**. Its solution explicitly reconstructs

\[
f(x,y)=x^3y^3+x^2-2y^2
\]

before evaluating endpoints. Yet the diagnostic's later progress capture shows source 2110 white and both components at 1. The diagnostic question and final progress assignments therefore already fail a simple rule that every correct demonstration immediately produces an ordinary positive displayed increment. See [diagnostic content](../../capture/multivariable/14111253/content.json); the machine-readable case evidence retains its original history and live-feedback paths.

## Consequence for estimation

Keep mathematical overlap stable across these episodes. Treat the late jump as a separate diagnostic/relearning state update, and the early reversal as unstable displayed state. Use persistence and ordinary within-context practice to estimate repeated-credit behavior; use this event to inform the revalidation mechanism. Do not increase the encompassing weight merely to force either observed jump into a one-step repetition-credit equation.

The evidence establishes the timeline, course context, correctness, and persistence. It does not expose the private state variable that was reassessed. The best working mechanism is **revalidation of component knowledge after diagnostic/course reassessment**, with ordinary credit applied separately. This is a concrete model choice, not a claim that the captured band equals an exact internal repetition count.
