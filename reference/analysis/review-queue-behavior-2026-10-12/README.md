# Review queues and failed-review follow-ups

October 12, 2026. Read-only audit of saved captures, supplemented by primary-source explanations. Run `python3 reference/analysis/review-queue-behavior-2026-10-12/analyze.py` from the project root to regenerate [evidence.json](evidence.json).

## All-review queues

| Captured account | Legacy snapshots | All-review snapshots | Five-review snapshots |
|---|---:|---:|---:|
| Foundations | 1,141 | 215 | 102 |
| Linear | 554 | 74 | 40 |
| Multivariable | 524 | 32 | 9 |
| Differential | 466 | 30 | 3 |
| Total | 2,685 | 351 | 154 |

There are 344 distinct account/task-list combinations among the all-review observations. Counts cover exact `question-capture/*/queue-after.json` and `question-capture-workers/*/*/queue-after.json` patterns, excluding repair subfolders and newer HTML dashboards. Snapshots are not independent episodes, and these totals include assessment remediation. Task IDs indicate creation, not completion order; they cannot establish the absence of earlier assessments.

For example, the [Linear queue after lesson 14069304](../../mathacademy/question-capture-workers/linear/14069304/queue-after.json) contains five reviews. Its saved recent completion list contains lessons and reviews, with no assessment entry. This supports the ordinary-backlog interpretation but is not a complete origin audit.

Justin Skycak's [January 2025 public reply](https://www.reddit.com/r/mathacademy/comments/1hv9twt/reviews_gone_wild_on_ma/) explicitly confirms temporary all-review dashboards during ordinary backlogs, with lessons made available about every 3–4 reviews. He excludes quiz follow-up reviews from this expectation. The original poster then checks their history and reports a lesson after three reviews. The [primary-source Gamification chapter](<../../The Math Academy Way/III-COGNITIVE-LEARNING-STRATEGIES/22-Gamification/22-Gamification.md#progress-vs-xp>) describes an average minimum lesson opportunity of about 25%. Neither source specifies the complete implementation or guarantees current behavior.

## Failed reviews

The saved audit finds four explicit legacy failures and three explicit failures in 789 modern post-activity records. Captures continue to accumulate, so reruns can change these counts. Classification uses an explicit saved failure status or terminal poor-performance message, rather than treating every nonpositive award as failure. Modern queues are parsed from saved dashboard Start-button links, excluding history and prerequisite links.

| Account / failed review | Topic | Immediate captured queue | Later captured same-topic work |
|---|---|---|---|
| Differential / 14066880 | 6686 | Three unrelated lessons | Not reconstructed across both capture formats |
| Differential / 14070331 | 6399 | Four unrelated lessons and another review | Not reconstructed across both capture formats |
| Differential / 14095492 | 6382, Fourier constant term | Assessment plus three unrelated lessons | Not reconstructed across both capture formats |
| Multivariable / 14094456 | 4144 | Three unrelated lessons and two other reviews | Not reconstructed across both capture formats |
| Foundations / 14114451 | 1955, partial derivative geometry | Three unrelated lessons and two other reviews | Review 14114565 succeeds for 7 XP; no same-topic lesson in between in the modern captures |
| Differential / 14119202 | 849, ellipse equations | One other review | Lesson 14123293 fails, lesson 14133341 fails, lesson 14134399 succeeds |
| Differential / 14141823 | 849, ellipse equations | Five unrelated lessons | Review 14147016 succeeds for 2 XP; no same-topic lesson in between in the modern captures |

Saved completion evidence: [14095492 state](../../mathacademy/question-capture-workers/differential/14095492/state.json), [14114451](../../mathacademy/capture/foundations/14114451/post-activity.json), [14119202](../../mathacademy/capture/differential/14119202/post-activity.json), [14141823](../../mathacademy/capture/differential/14141823/post-activity.json). The legacy completion screenshot was also inspected and confirms the halt and -1 XP award.

These sequences demonstrate varied recovery and continued unrelated activity after failures. They do not prove a universal immediate lesson replacement. Modern chronology uses first completion-observation timestamps, not task creation IDs. Subsequent captures need not cover every intervening action, and the first observed queue is not necessarily the exact first backend refresh.

The [Practice Experience remediation section](<../../The Math Academy Way/VI-FREQUENTLY-ASKED-QUESTIONS/FAQ-The-Practice-Experience/FAQ-The-Practice-Experience.md#remediation>) explicitly describes full lessons after failed **key-prerequisite remedial reviews**. That is not proof that every ordinary or quiz-remediation review follows the same rule. Review origin and required status are not classified in this audit, so assessment-specific failure and clearance remain unestablished.

### Assessment-origin check

The follow-up [assessment-review failure check](assessment-review-failure-check.json) examines 50 distinct reviews linked to missed assessment topics in the existing retake audit. Forty-five have explicit passed status; the other five have successful completion messages without an outcome field. None records a failure. Direct post-assessment queue scans do not link any of our seven explicitly failed reviews to an assessment. Recorded missed assessment topics likewise have no same-account overlap with those failures, including the 14 newer assessment captures checked here.

This provides no directly observed assessment-required review failure sequence. It does not imply that the branch never occurs; incomplete history can omit it. Successful remediation sequences establish the normal path, while the seven other failures establish that review recovery can vary. Neither observation settles the assessment-failure branch.

Our capture worker also intentionally chooses answer patterns and repeats some failed activities. Those choices affect which follow-up gets completed; a selected retry is not proof that Math Academy required it.

## Consequence for our proposal

Allow all-review queues without permanently reserving a lesson slot. The chosen rule is to offer an eligible optional lesson after three finished ordinary review attempts without a lesson offer. Passed and failed attempts count; reset when the ordinary queue offers an eligible lesson. No separate backlog-size threshold is needed. If no lesson is eligible, retain the pending offer until one becomes available. Required assessment remediation takes precedence and is excluded from the ordinary-review count. Three is our selected default informed by the staff explanation.

The chosen policy distinguishes regular reviews from remediation. A failed ordinary review updates learner accuracy and retention state, then ends without a forced follow-up; later reviews follow normal due-date and priority scheduling. A failed remediation review requires the full lesson on that topic, whether the origin is an assessment or two lesson failures at the same KP without further progress. The linked lesson preserves the original gate: assessment remediation blocks unrelated study, while prerequisite repair blocks the original learning path. Passing the replacement lesson clears that topic's obligation without an extra automatic review. This is an explicit product choice informed by the captures and documented prerequisite escalation; the assessment-specific transition has not been directly observed. Exact retention effects remain calibration work. Learner-state updates do not change shared question-difficulty selection weights.
