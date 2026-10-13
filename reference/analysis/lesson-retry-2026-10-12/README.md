# Failed lesson retry timing

October 12, 2026. Read-only analysis of saved account captures; no engine or database changes. Run `python3 reference/analysis/lesson-retry-2026-10-12/analyze.py` from the project root to regenerate [evidence.json](evidence.json). Capture files continue to accumulate, so later runs can change the sample.

## What the documentation establishes

The [official FAQ](https://mathacademy.com/faq) says a failed lesson returns within a few days. The [algorithm description](https://mathacademy.com/how-our-ai-works) says the learner can work on unrelated topics before trying the failed lesson again; another failure without further progress triggers targeted prerequisite reviews. The [local primary-source remediation chapter](<../../The Math Academy Way/III-COGNITIVE-LEARNING-STRATEGIES/21-Targeted-Remediation/21-Targeted-Remediation.md>) explains the break and progress on other learning paths. The [Gamification chapter](<../../The Math Academy Way/III-COGNITIVE-LEARNING-STRATEGIES/22-Gamification/22-Gamification.md>) explicitly describes delayed attempts with changed questions.

These sources establish a pause, unrelated progress, and later retry. They do not publish a fixed number of hours, XP, or intervening activities. The FAQ describes a return window, not a minimum multi-day wait.

## Captured returns

The initial saved run contains 15 explicit failed lessons, with later same-topic lesson offers and attempts for 14. Twelve of those offers appear after 5–11 other captured completed activities. Two much later offers follow 71 and 772 captured activities; these cannot establish the initial cooldown. One failure has no observed later offer despite substantial other work, showing that a minimum activity count alone does not guarantee dashboard placement.

The closest traces are:

| Account / failed task | First observed retry offer after other activities | Captured practice XP | Elapsed from failure observation to offer | What the preceding queue showed |
|---|---:|---:|---:|---|
| Foundations / 14041842 | 5 reviews | 13 | About 15 minutes | No retry after 4 activities |
| Differential / 14068149 | 3 lessons + 2 reviews | 40 | About 34 minutes | No retry after 4 activities |
| Linear / 14108275 | 1 lesson + 4 reviews | 25 | About 18 minutes | No retry after 4 activities |
| Linear / 14132257 | 6 attempts, including one failed lesson | 22 | About 69 minutes | No retry after 5 attempts, including the failure; the next successful lesson supplies the fifth successful practice activity |

Representative evidence: [Foundations return queue](../../mathacademy/question-capture/14069126/queue-after.json), [Differential return queue](../../mathacademy/question-capture-workers/differential/14068558/queue-after.json), [Linear failed lesson](../../mathacademy/capture/linear/14108275/post-activity.json), and [Linear retry's completed capture](../../mathacademy/capture/linear/14114517/post-activity.json). The structured evidence links the first-offer dashboards and last-absent queues for every traced failure.

The recorded elapsed times are observation differences, not exact backend cooldowns. Completion observations can follow actual completion; legacy queues use approximate associated progress-capture times. The modern Linear failure and its return both occur within the same overnight capture session, so a universal 24- or 48-hour minimum is incompatible with this sequence. The 13-XP return also contradicts any universal minimum above 13 captured XP, provided the captured intervening history is complete.

Other returns after six, seven, nine, or eleven activities show that five cannot be treated as an exact display guarantee. Normal recommendation ranking, prerequisite readiness, required assessments/remediation, course changes, and capture gaps can postpone visibility. The five-activity interpretation is an inferred eligibility rule, not a recovered server parameter.

The two failed ellipse lessons in Differential also stop at different KPs: 14123293 reaches the tall-ellipse KP, while 14133341 stops at the earlier wide-ellipse KP. They do not directly demonstrate two failures at the same KP and should not be used to claim that the documented prerequisite trigger was ignored.

Thirteen of the fourteen observed retry pairs share no captured question IDs; one pair shares one. Our accepted fresh-question rule remains stricter than that exception. The capture worker's all-correct retry instructions influence which offered task gets selected and its results; they do not establish the source scheduler's delay.

## Chosen starting rule

After a first failed lesson, defer its automatic retry until **five other practice activities have successfully completed**. Count lessons, reviews, and assignments/multisteps on other topics; do not count the failed attempt, unfinished work, supply deferrals, or other failures. Then admit a fresh-question retry to normal recommendation ranking, subject to prerequisite readiness, available questions, and existing required-work gates. Do not add a fixed XP threshold or minimum number of hours.

Derive the count from finalized activity history after the failure; do not maintain another stored progress balance. This rule is simple, fits the closest observed return brackets, and permits unrelated progress. The user approved it as the starting policy; implementation remains necessary. The already chosen two-failures-at-the-same-KP escalation still applies instead of another ordinary retry when its condition is met.

This rule concerns automatic lesson offers. It does not add a new restriction on voluntary study. First-offer timing cannot answer every direct-start UI policy.

The user also approved a five-successful-activities break after a required replacement lesson fails. Preserve the original obligation. Other ready required remediation comes first; if all remaining required work is waiting, temporarily permit ordinary study. Successful practice on other topics advances the break, while failures do not. At five successes, the eligible fresh-question lesson becomes required again. Its associated assessment retake remains unavailable until the linked review or replacement lesson passes. Passing unrelated work advances the break without clearing remediation. Repeated failure at the same KP without progress triggers the chosen prerequisite escalation. This required-lesson branch is an explicit product choice rather than a directly observed capture sequence.
